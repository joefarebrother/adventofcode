from heapq import heappush, heappop
from typing import Callable
from collections import deque, defaultdict
from itertools import chain
import math


class AbGraph():
    """
    An abstract class for implementing various graph search operations.

    During such traversals, self.prev is a dict to help reconstruct path info.
    Traversals yield (n, d) for node n at distance d from the start.
    """

    def __init__(self):
        self.prev = {}
        self.dists = {}
        self.queue = None
        self.pqueue = None

    def adj(self, _node):
        """
        Given a node, should return an iterator of its adjacent nodes.
        If this is an weighted graph (i.e. you're using dijkstra/astar) then it should be a dict of adjacent nodes to distances.
        """
        return {}

    def key(self, node):
        """
        Should return a key used to identify the node. Two nodes are considered equal to search functions if they
        Can be used to propagate additional information in the node.
        """
        return node

    def __getitem__(self, node):
        return self.adj(node)

    def dist1(self):
        """
        Returns a graph with the same adjacency function except that assigns a distance of 1 to each node.
        """
        class D1Gr(AbGraph):
            def __init__(self, inner):
                self._inner = inner
                super().__init__()

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
                super().__init__()

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
        if end is not None:
            yield (self.key(k) if keys_only else end)

    def get_path(self, end, keys_only=False):
        """
        After a graph search has completed, generates the path it saved from start to the end.
        If keys_only is True, key is called on the each node of the path.
        """
        return reversed(list(self.get_rev_path(end, keys_only)))

    def DFS(self, start):
        """
        Traverses the graph in a depth first order.
        Distances are ignored and treated as 1.
        """
        self.prev = {}

        def trav(node, d, prev):
            k = self.key(node)
            if k not in self.prev:
                self.prev[k] = prev
                yield node, d
                for nxt in self[node]:
                    yield from trav(nxt, d+1, node)

        return GraphSearchResult(self, trav(start, 0, None))

    def topsort(self, start) -> list:
        """
        Returns the nodes reachable from start in a topologically sorted order.
        """
        return [n for (n, d) in self.DFS(start)]

    def leaves(self, start):
        """
        Computes the leaves (nodes with no adjacent nodes) reachable from the start.
        """
        for (node, _) in self.DFS(start):
            if not self.adj(node):
                yield node

    def BFS(self, start):
        """
        Traverses the graph in a breadth-first order.
        Distances are ignored and treated as 1.

        While running, self.queue is set to the queue. Shouldn't be modified - just for debugging purposes.
        """
        # node, dist, prev
        queue = deque([(start, 0, None)])
        self.queue = queue
        self.prev = {}

        def go():
            while len(queue) > 0:
                node, d, prev = queue.popleft()
                if self.key(node) not in self.prev:
                    self.prev[self.key(node)] = prev
                    yield (node, d)

                    for nxt in self[node]:
                        k = self.key(nxt)
                        if k not in self.prev:
                            queue.append((nxt, d+1, node))

        return GraphSearchResult(self, go())

    def astar(self, start, h=lambda _: 0, incon_cb=lambda x, y: None):
        """
        Traverses the graph using A*/Dijkstra's algorithm.

        h is the heuristic function, approximating distance to the goal.
        When constant, it's dijkstra's.
        Should be admissible (doesn't overapproximate total distance to the goal) in order to return optimal distances.
        When consistent (i.e. h(x) <= d(x,y) + h(y)), it's admissible, and the algorithm is optimally efficient.
        Calls incon_cb the first time it detects that the heuristic is inconsistent.

        While running, self.pqueue is set to the priority queue, and self.dists is set to the distances map.
        These shouldn't be modified.
        """
        # (d(start, x) + h(x), d(start, x), tiebreak, x, prev)
        pqueue = [(h(start), 0, 0, start, None)]
        self.pqueue = pqueue

        dists = {self.key(start): 0}
        self.dists = dists
        self.prev = {}

        def go():
            i = 0
            warned = False
            while len(pqueue) > 0:
                _, d, _, node, prev = heappop(pqueue)
                if dists[self.key(node)] < d or self.key(node) in self.prev:
                    continue

                self.prev[self.key(node)] = prev
                yield (node, d)

                for nxt, nd in self[node].items():
                    k = self.key(nxt)
                    if k in dists and dists[k] <= d+nd:
                        continue
                    if not warned:
                        hx = h(node)
                        hy = h(nxt)
                        if hx > nd + hy:
                            warned = True
                            print("Warning: heuristic not consistent: x=",
                                  node, " y=", nxt, "d=", nd, "hx-hy=", hx-hy, "hx=", hx, "hy=", hy)
                            incon_cb(node, nxt)
                    dists[k] = d+nd
                    i += 1
                    heappush(pqueue, (d+nd+h(nxt), d+nd, i, nxt, node))
        return GraphSearchResult(self, go())

    dijkstra = astar

    def DAG_search(self, start, end):
        """
        If the graph is acyclic, finds the shortest path from start to end.

        Returns:
        - (endpoint, d) if end was found at dist d from the start
        - (None, None) otherwise
        """
        self.prev = {}
        cache = {}
        sent = object()

        def go(s):
            if _is_end(end, s):
                return (0, [s])
            k = self.key(s)
            if k in cache:
                r = cache[k]
                if r is sent:
                    raise Exception("Graph has a cycle", s)
                return r
            cache[k] = sent
            mind = math.inf
            minp = None
            for nxt, d in self[s].items():
                nd, np = go(nxt)
                nd += d
                if nd < mind:
                    mind = nd
                    minp = [s]+np
            cache[k] = mind, minp
            return mind, minp
        d, ps = go(start)
        if d < math.inf:
            for p, n in zip(ps, ps[1:]):
                self.prev[n] = p
            return ps[-1], d
        return (None, None)


class GraphSearchResult:
    def __init__(self, graph, it):
        self.graph = graph
        self.it = it
        self.max_dist = 0

    def __iter__(self):
        for (n, d) in self.it:
            self.max_dist = max(self.max_dist, d)
            yield (n, d)

    def exhaust(self):
        """Exhausts the full search space."""
        for _ in self:
            pass
        return self

    def find(self, end_cond):
        """
        Finds the given end point. This can be a value that's compared for equality, or a function.
        Returns (n,d) where n is the node reached and d is the distance; or (None, math.inf) if no end was reached.
        """
        for n, d in self:
            if _is_end(end_cond, n):
                return (n, d)
        return (None, math.inf)

    def dist(self, end_cond):
        """
        Returns the distance to the given end point, or math.inf if it could not be found.
        """
        return self.find(end_cond)[1]

    def all_dists(self):
        """Exhausts the search space and returns the full distances map"""
        self.exhaust()
        return self.graph.dists


def _is_end(end, node):
    if end is None:
        return False
    elif callable(end):
        return end(node)
    else:
        return end == node


class FGraph(AbGraph):
    """
    Graph constructed with its adjacency function.
    """

    def __init__(self, adj: Callable, key=None):
        super().__init__()
        self._adj = adj
        self._key = key

    def adj(self, node):
        return self._adj(node) or {}

    def key(self, node):
        if self._key is not None:
            return self._key(node)
        return node


class DGraph(AbGraph):
    """
    Graph whose adjacency function is specified by a dict.
    """

    def __init__(self, adj: dict, key=None):
        super().__init__()
        self._adj = adj
        self._key = key

    def adj(self, node):
        return self._adj[node] if node in self._adj else {}

    def key(self, node):
        if self._key is not None:
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
        Computes the symmetric graph (with each arrow being replaced by an arrow in both directions)
        """
        return self | self.reverse()
