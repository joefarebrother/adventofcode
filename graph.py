from heapq import heappush, heappop
from typing import Callable
from collections import deque, defaultdict
from itertools import chain


class AbGraph():
    """
    An abstract class for implementing various graph search operations.

    During such traversals, self.prev is a dict to help reconstruct path info.
    Each generator yields (n, d) for node n at distance d from the start.
    """

    def __init__(self):
        self.prev = {}
        self.dists = {}

    def adj(self, node):
        """
        Given a node, should return an iterator of its adjacent nodes.
        If this is an weighted graph (i.e. you're using dijkstra/astar) then it should be a dict of adjacent nodes to distances.
        """
        return {}

    def key(self, node):
        """
        Should return a key used to identify the node. Two nodes are considered equal to search functions if they
        Can be used to propegate additional information in the node.
        """
        return node

    def __getitem__(self, node):
        return self.adj(node)

    def dist1(self):
        """
        Returns a graph with the same adjacncy function except that assigns a distance of 1 to each node.
        """
        class D1Gr(AbGraph):
            def __init__(self, inner):
                self._inner = inner

            def adj(self, node):
                return {n: 1 for n in (self._inner.adj(node) or [])}

            def key(self, node):
                return self._inner.key(node)

        return D1Gr(self)

    def __or__(self, other):
        class UGraph(AbGraph):
            def __init__(self, g1, g2):
                self._g1 = g1
                self._g2 = g2

            def adj(self, node):
                a1 = self._g1.adj(node)
                a2 = self._g2.adj(node)
                if isinstance(a1, dict) and isinstance(a2, dict):
                    res = defaultdict(int)
                    res.update(a1)
                    for (k, v) in a2.items():
                        res[k] = min(res[k], v)
                    return res
                else:
                    return chain(a1, a2)

            def key(self, node):
                return self._g1.key(node)
        return UGraph(self, other)

    def get_rev_path(self, end, keys_only=False):
        """
        After a graph search has completed, generates the path it saved from end to the start.
        If keys_only is True, key is called on the each node of the path.
        """
        while (k := self.key(end)) in self.prev:
            yield (k if keys_only else end)
            end = self.prev[k]

    def DFS_gen(self, start):
        """
        A generator that yields the nodes reachable from start in a depth first order along eith their distances.
        """
        self.prev = {}

        def trav(node, d, prev):
            k = self.key(node)
            if k not in self.prev:
                self.prev[k] = prev
                yield node, d
                for next in self[node]:
                    yield from trav(next, d+1, node)

        yield from trav(start, 0, None)

    def DFS(self, start, end=None):
        """
        Traverses the graph in a depth first order until end is found or the search space is exhausted.

        Returns (endpoint, d) if an endpoint was found d steps from the start, and (None, d) if it wasn't and d is the maximum depth.
        """
        return _consume(self.DFS_gen(start), end)

    def topsort(self, start) -> list:
        """
        Returns the nodes reachable from start in a topologically sorted order.
        """
        return [n for (n, d) in self.DFS_gen(start)]

    def leaves(self, start):
        """
        Computes the leaves (nodes with no adjacent nodes) reachable from the start.
        """
        for (node, _) in self.DFS_gen(start):
            if not self.adj(node):
                yield node

    def BFS_gen(self, start):
        """
        A generator that yields nodes reachable from start in a breadth first order along.

        While running, self.queue is set to the queue. Shouldn't be modified - just for debugging purposes.
        """
        # node, dist, prev
        queue = deque([(start, 0, None)])
        self.queue = queue
        self.prev = {}

        while len(queue) > 0:
            node, d, prev = queue.popleft()
            self.prev[self.key(node)] = prev
            yield (node, d)

            for next in self[node]:
                k = self.key(next)
                if k not in self.prev:
                    queue.append((next, d+1, node))

    def BFS(self, start, end=None):
        """
        Traverses the graph in a breadth first order until end is reached or until the search space is exhausted.
        end may be a predicate, a value (in which case it's compared to node), or None.

        Returns
         (endpoint, d) if and endpoint end is found and d is the distance to it,
         (None, d) if the endpoint wasn't found and d is the maximum distance encountered.
        """
        return _consume(self.BFS_gen(start), end)

    def astar_gen(self, start, h=lambda _: 0):
        """
        A generator that traverses the graph sing the A* algorithm / dijkstra's algorithm.

        h is the heiristic function, aproximating distance to the goal.
        When constant, it's djikstra's.
        When consistent (i.e. h(x) <= d(x,y) + h(y)) the distances returned are optimal.

        While running, self.pqueue is set to the priority queue, and self.dists is set to the distances map.
        These shouldn't be modified.
        """
        # (d(start, x) + h(x), d(start, x), tiebreak, x, prev)
        pqueue = [(h(start), 0, 0, start, None)]
        self.pqueue = pqueue
        i = 0
        dists = {self.key(start): 0}
        self.dists = dists
        self.prev = {}
        while len(pqueue) > 0:
            _, d, _, node, prev = heappop(pqueue)
            if dists[self.key(node)] < d:
                continue

            self.prev[self.key(node)] = prev
            yield (node, d)

            for next, nd in self[node].items():
                k = self.key(next)
                if k in dists and dists[k] <= d+nd:
                    continue
                dists[k] = d+nd
                i += 1
                heappush(pqueue, (d+nd+h(next), d+nd, i, next, node))

    dijkstra_gen = astar_gen

    def astar(self, start, end, h=lambda _: 0):
        """
        Traverses the graph using the A* algorithm / djikstra's algorithm entil the end is reached or the search space is exhausted.
        end may be a predicate, a value (in which case it's compared to node), or None.

        h is the heiristic function, aproximating distance to the goal.
        When constant, it's djikstra's.
        When consistent (i.e. h(x) <= d(x,y) + h(y) - this is an underapproximation) the distances returned are optimal.

        Returns:
        - (endpoint, d) if end was found at distance d from the start.
        - (None, dists) if end was not found, and dist is the distances map.
        """
        return _consume(self.astar_gen(start, h), end, lambda: self.dists)

    dijkstra = astar


def _consume(gen, end, onfail=None):
    maxd = 0
    for n, d in gen:
        if _is_end(end, n):
            return (n, d)
        maxd = max(d, maxd)
    return (None, onfail() if onfail else maxd)


def _is_end(end, node):
    if end == None:
        return False
    elif callable(end):
        return end(node)
    else:
        return end == node


class FGraph(AbGraph):
    """
    Graph constructed with its asjancency function.
    """

    def __init__(self, adj: Callable, key=None):
        self._adj = adj
        self._key = key

    def adj(self, node):
        return self._adj(node) or {}

    def key(self, node):
        if self._key != None:
            return self._key(node)
        return node


class DGraph(AbGraph):
    """
    Graph whose adjacency function is specified by a dict.
    """

    def __init__(self, adj: dict, key=None):
        self._adj = adj
        self._key = key

    def adj(self, node):
        return self._adj[node] if node in self._adj else {}

    def key(self, node):
        if self._key != None:
            return self._key(node)
        return node

    def reverse(self):
        """
        Computes the reverse graph (with the arrows pointing in the opposite direction).
        """
        res = defaultdict(lambda: defaultdict(dict))
        for (a, adj) in self._adj.items():
            if isinstance(adj, dict):
                for (b, d) in adj.items():
                    res[b][a] = d
            else:
                for b in adj:
                    res[b][a] = 1
        return DGraph(res, self.key)

    def sym(self):
        """
        Computes the symetric graph (with each arrow being replaced by an arrow in both directions)
        """
        return self | self.reverse()
