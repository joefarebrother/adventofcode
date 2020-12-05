from functools import reduce
from collections import deque, defaultdict
from heapq import heappush, heappop
import math
import os
import re
from attrdict import AttrDict
from typing import List, Tuple, Callable, Iterable, Optional
from geom import Rectangle, bounding_box, convert_pos, neighbours, intersect_irange
from grid import Grid

block_char = '█'


def sign(x) -> int:
    """Returns the sign of x"""
    if x < 0:
        return -1
    if x > 0:
        return 1
    return 0


def egcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Performs the extended Euclidian algorithm.
    Returns (g, x, y) such that x*a + y*b = g, and g = gcd(a, b).
    """
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def mod_inv(a: int, m: int) -> int:
    """Returns the inverse of a modulo m"""
    g, x, _ = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def lcm(*xs) -> int:
    """
    Returns the least common multiple of the arguments.
    This exists in math in python 3.9, but I don't have that.
    """
    def lcm2(x: int, y: int) -> int:
        return x * y // math.gcd(x, y)

    return reduce(lcm2, xs, 1)


foldr = reduce


def clear_screen() -> None:
    """Clears the screen of the terminal"""
    print(chr(27) + "[2J")


def mapl(f: Callable, *xs) -> list:
    """Like map but returns a list"""
    return list(map(f, *xs))


def ints(xs: list) -> List[int]:
    """Casts each element of xs to an int"""
    return mapl(int, xs)


def mint(x, default=None):
    """Maybe int - casts to int and returns default on failure"""
    try:
        return int(x)
    except ValueError:
        return default


def ints_in(x: str, allow_neg=False) -> List[int]:
    """Finds and parses all integers in the string x"""
    ex = r'-?\d+' if allow_neg else r'\d+'
    return ints(re.findall(ex, x))


def match(regex: str, text: str, exact=True, ints=True, onfail=None):
    """
    Matches the given regex against the given string, and returns the capture groups.
    If the match succeeds but there were no capture groups, returns True.
    Returns onfail if the match failed.
    exact determines whether the whole string must be matched, and ints determines whether to parse integers from the result.
    """
    f = re.fullmatch if exact else re.search
    m = f(regex, text)
    if not m:
        return onfail
    grs = list(m.groups())
    if len(grs) == 0:
        return True

    if ints:
        grs = [mint(x, x) for x in grs]

    return grs


def modify_idx(xs, i: int, v):
    """
    When xs is a list or tuple, return a new list or tuple with the item at index i being changed to v
    """
    if isinstance(xs, list):
        ty = list
    elif isinstance(xs, tuple):
        ty = tuple
    else:
        raise TypeError("Expected list or tuple", type(xs), xs)

    new = [x for x in xs]
    new[i] = v
    return ty(new)


def ident(x):
    """The identity function."""
    return x


# TODO: Refactor these graph search functions to a common class

def BFS(start, adjfun, end=None, key=ident):
    """
    Performs a breadth-first search.

    Arguments:
    - start: the root of the search
    - adjfun: the function called to determine the adjacent nodes.
        Sould return an iterable or None.
    - end: The end point of the search.
        If it's a function, the search ends when it returns True for a node.
        Otherwise, the search ends when the node is equal to end.
    - key: The key function, used to determine whether two nodes should be treated as equal.

    Returns:
    - (True, d) if end was found and was distance d from the start.
    - (False. d) if end was not found, and d is the maximum distance from the start to any node.

    Variables accessible during calls to each user-provided function:
    - BFS.dist: The distance to the node under consideration.
    - BFS.queue: The queue. Should not be mutated.
    """
    queue = deque([(start, 0)])
    visited = {key(start)}
    d = 0
    while len(queue) > 0:
        p, d = queue.popleft()

        if (callable(end) and end(p)) or end == p:
            BFS.queue = None
            BFS.dist = 0
            return (True, d)
        BFS.queue = queue
        BFS.dist = d
        next = adjfun(p)
        if next != None:
            for n in next:
                if key(n) in visited:
                    continue
                visited |= {key(n)}
                queue += [(n, d+1)]
    BFS.queue = None
    BFS.dist = 0
    return (False, d)


def astar(start, adjfun, end=None, key=ident, h=lambda _: 0):
    """
    Performs the A-star algorithm / dijkstra's algorithm.

    Arguments:
    - start: the root of the search
    - adjfun: the function called to determine the adjacent nodes.
        Sould return an iterable or None.
        The returned iterable should produce (node, distance) pairs.
    - end: The end point of the search.
        If it's a function, the search ends when it returns True for a node.
        Otherwise, the search ends when the node is equal to end.
    - key: The key function, used to determine whether two nodes should be treated as equal.
    - h: The heuristic function.

    Returns:
    - (True, d) if end was found at distance d from the start.
    - (False, dists) if end was not found.
        dists contains the distances from the start of each node seen.

    Variables accessible during calls to each user-provided function:
    - astar.dist: The distance from the start to the node under consideration.
    - astar.dists: The best known distatances from the start of the queue to each node seen so far.
    - astar.pqueue: The priority queue. Should not be mutated.
    """
    pqueue = [(h(start), 0, 0, start)]
    i = 0
    dists = {key(start): 0}
    while len(pqueue) > 0:
        _, d, _, p = heappop(pqueue)
        if dists[key(p)] < d:
            continue

        if (callable(end) and end(p)) or end == p:
            astar.pqueue = None
            astar.dists = None
            astar.dist = 0
            return (True, d)

        astar.pqueue = pqueue
        astar.dists = dists
        astar.dist = d
        next = adjfun(p)
        if next != None:
            for n, nd in next:
                if key(n) in dists and dists[key(n)] <= d+nd:
                    continue
                dists[key(n)] = d+nd
                i += 1
                heappush(pqueue, (d+nd+h(n), d+nd, i, n))

    astar.pqueue = None
    astar.dists = None
    astar.dist = 0
    return(False, dists)


dijkstra = astar


def bin_search(lo, hi, f: Callable):
    """
    Performs a binary search on an abstract search space.

    Arguments:
    - lo: The low endpoint.
    - hi: The high endpoint. Can be None to represent infinity.
    - f: A monotone-decreasing function int->bool; i.e. goes 11110000

    Returns:
    - The unique int target in the range [lo, hi) such that f = (lambda i: i <= target) on this range.
      In other words, the unique target such that f(target) and not f(target+1)

    Example:
    - If xs is a sorted list, bin_search(0, len(xs), lambda i: xs[i]<=n) returns the index of n in xs.
    """

    if (not (hi == None or lo < hi)):
        raise Exception("Empty range")

    if not f(lo):
        return lo

    if(hi == None):
        hi = lo*2 if lo > 0 else 32
        while(f(hi)):
            (lo, hi) = (hi, lo*2)

    # Invariant: lo <= target < hi; i.e. f(lo) and not f(hi)
    # This invariant is not completely checked at the start; since f might be undefined on hi.
    # However, it still holds if we assume f "would be" false beyond its range.

    while(hi - lo > 1):
        mid = (lo+hi)//2
        if f(mid):
            lo = mid
        else:
            hi = mid

    return lo


def readlines(filename: str) -> List[str]:
    """
    Returns the list of lines in the given file. Strips the trailing newline on each.
    """
    return [l[:-1] for l in open(filename)]


def irange(*args) -> range:
    """Inclusive range"""
    args = list(args)
    if len(args) == 1:
        args[0] += 1
    else:
        args[1] += 1
    return range(*args)


def submit(answer: int, part=1, day=None, year=2020, confirm=True) -> None:
    """
    Submits the answer to the AOC server, then exits. Asks for confirmation first if confrm is set.
    Use with caution, as an incorrect answer will lock you out for a minute.
    """
    if confirm:
        print(f"Submit {answer} to part {part}? (y/n)")
        if input()[0] != "y":
            return

    cmd = f"./submit {part} {answer}"
    if(day):
        cmd += f" {str(day)} {str(year)}"
    os.system(cmd)
    exit()
