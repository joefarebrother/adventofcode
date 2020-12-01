from collections import deque, defaultdict
from heapq import heappush, heappop
import math
import os


block_char = '█'


def draw_grid(grid, symbols=None, flipx=False, flipy=False):
    """
    Draws the given grid to the screen.

    grid may be a list of lists (in which case each element is a row, printed top to bottom) or a dict.
    If grid is a dict, its keys may either be complex numbers or (x, y) pairs.
    In this case, positive y values are interpreted as higher.
    """

    if symbols == None:
        symbols = {0: ' ', 1: '█'}

    if not isinstance(symbols, dict):
        symbols = {i: v for i, v in enumerate(symbols)}

    if type(grid) == list:
        grid = grid_to_cplx(grid)

    if not isinstance(grid, dict):
        raise Exception("draw_grid: Expected list or dict")

    coords = grid.keys()
    if len(coords) == 0:
        return
    if type(list(coords)[0]) == complex:
        xcoords = [int(z.real) for z in coords]
        ycoords = [int(z.imag) for z in coords]
    else:
        xcoords = [x for (x, y) in coords]
        ycoords = [y for (x, y) in coords]

    yrange = range(min(ycoords), max(ycoords)+1)
    if not flipy:
        yrange = reversed(yrange)

    xrange = range(min(xcoords), max(xcoords)+1)
    if flipx:
        xrange = reversed(xrange)

    res = ''
    for y in yrange:
        for x in xrange:
            if type(list(coords)[0]) == complex:
                coord = (x+y*1j)
            else:
                coord = (x, y)
            elt = grid[coord] if coord in grid else ' '
            sym = symbols[elt] if elt in symbols else str(elt)[0]
            res += sym
        res += '\n'

    print(res)


def grid_to_cplx(grid):
    """
    Converts a grid represented as a list of lists into o defaultdict with complex-valued keys.
    The outer list is first reversed, so that higher imaginary values correspond to "up".
    """
    cgrid = defaultdict()
    for y, line in enumerate(reversed(grid)):
        for x, c in enumerate(line):
            cgrid[x+y*1j] = c

    return cgrid


def sign(x):
    """Returns the sign of x"""
    if x < 0:
        return -1
    if x > 0:
        return 1
    return 0


def egcd(a, b):
    """
    Performs the extended Euclidian algorithm.
    Returns (g, x, y) such that x*a + y*b = g, and g = gcd(a, b).
    """
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def mod_inv(a, m):
    """Returns the inverse of a modulo m"""
    g, x, _ = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def clear_screen():
    """Clears the screen of the terminal"""
    print(chr(27) + "[2J")


def mapl(f, *xs):
    """Like map but returns a list"""
    return list(map(f, *xs))


def ints(xs):
    """Casts each element of xs to an int"""
    return mapl(int, xs)


def neighbours(p):
    """
    When p is a complex number with integer components, returns the four orthagonal neighbours of p.
    """
    return [p+1j**dir for dir in range(4)]


def ident(x):
    """The identity function."""
    return x


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
    - (d, True) if end was found and was distance d from the start.
    - (d, False) if end was not found, and d is the maximum distance from the start to any node.

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
            return (d, True)
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
    return (d, False)


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
    - astar.dists: The best known distatances of from the start of the queue to each node seen so far.
    - astar.pqueue: The priority queue. Should not be mutated.
    - 
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


def submit(answer, day=None, year=2020):
    """
    Submits the answer to the AOC server, then exits.
    Use with caution, as an incorrect answer will lock you out for a minute.
    """
    cmd = "./submit " + str(answer)
    if(day):
        cmd += f" {str(day)} {str(year)}"
    os.system(cmd)
    exit()
