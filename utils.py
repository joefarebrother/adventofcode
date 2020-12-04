from collections import deque, defaultdict
from heapq import heappush, heappop
import math
import os
import re
from attrdict import AttrDict

block_char = '█'


class Rectangle:
    """
    A rectangle.

    Constructed by specifying two opposite corners as either (x,y) tuples or complex numbers. These points are inclusive.

    Supports addition of points and other rectangles.
    """

    def __init__(self, p0, p1):
        (x0, y0) = convert_pos(p0)
        (x1, y1) = convert_pos(p1)

        self.minx, self.maxx = min(x0, x1), max(x0, x1)
        self.miny, self.maxy = min(y0, y1), max(y0, y1)

    def width(self):
        """
        Returns the width of this rectangle.
        """
        return self.maxx-self.minx+1

    def height(self):
        """
        Returns the height of this rectangle.
        """
        return self.maxy-self.miny+1

    def xrange(self):
        """
        Returns the range of x-positions this rectangle spans.
        """
        return range(self.minx, self.maxx+1)

    def yrange(self):
        """
        Returns the range of y-positions this rectangle spans.
        """
        return range(self.miny, self.maxy+1)

    def __contains__(self, pos):
        (x, y) = convert_pos(pos)
        return x in self.xrange() and y in self.yrange()

    def corners(self, type=complex):
        """
        Returns the 4 corners of this rectangle, as positions of the given type. Order unspecified.
        """
        minx, miny, maxx, maxy = self.minx, self.miny, self.maxx, self.maxy
        corners = [(minx, miny), (minx, maxy), (maxx, maxy), (maxx, miny)]
        if type == tuple:
            return corners
        else:
            return mapl(lambda p: _pos_as(p, type), corners)

    def opposite_corners(self, type=complex):
        """
        Returns the 2 opposite corners with the min/max x/y positions.
        """
        minx, miny, maxx, maxy = self.minx, self.miny, self.maxx, self.maxy
        corners = [(minx, miny), (maxx, maxy)]
        if type == tuple:
            return corners
        else:
            return mapl(lambda p: _pos_as(p, type), corners)

    def __add__(self, other):
        if isinstance(other, Rectangle):
            (p0, p1) = other.opposite_corners()
            return (self + p0) + p1
        else:
            if other in self:
                return self
            return bounding_box(self.opposite_corners() + [other])


def bounding_box(points):
    """
    Computes the bounding box of the given points.
    """
    points = mapl(convert_pos(points))
    if len(points) == 0:
        return None

    xs = [x for (x, y) in points]
    ys = [y for (x, y) in points]

    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)

    return Rectangle((minx, miny), (maxx, maxy))


def convert_pos(pos, to_ints=False):
    """
    Converts the given position to the type used internally; (x,y) tuples.
    Supported position types are complex numbers, and length 2 tuples/lists.
    """
    if isinstance(pos, complex):
        pos = (pos.real, pos.imag)
    if isinstance(pos, tuple) or isinstance(pos, list):
        if len(pos) != 2:
            raise Exception("Expected a position of length 2", pos)
    else:
        raise TypeError("Unsupported position type", type(pos), pos)
    return tuple(map(int, pos)) if to_ints else tuple(pos)


def _pos_as(pos, type):
    """
    Converts the given position from an (x,y) tuple to the given type. Supported types are complex and tuple.
    """
    if type == tuple:
        return pos
    elif type == complex:
        (x, y) = pos
        return x + y*1j
    else:
        raise Exception("Unknown position type", type)


class Grid:
    """
    A grid that can be indexed with either (x,y) pairs or complex numbers.

    Constructor arguments:
    - grid: Determines the initial data.
        Can be a another Grid, a list (of rows which are lists or strings), or a dict (with keys being either complex or (x,y) tuples)
        Data is copies and isn't aliased.
        Can also be a string, which will be treated as a filenane, where the lines will be rows.
    - y_is_down: Whether a higher y index is to be interpreted as down.
        The default is determined by the type of grid: If it's a list/file, it's True, if it's a dict its False, and if its' a Grid it's copied.
        If it's set to False when its a list, the bottom left corner will be (0,0), rather than the top left.
        Otherwise, it only matters for printing.
    - wrapx, wrapy: Determines whether to wrap in the given direction, making the grid into a cylinder or torus.
        Grid indicies must be in the range [0, width/height)
        If data is initialised from a dict or another Grid, this should be a positive integer, False, or None. An integer represents an explicit width/height.
        If it's initialised from a list, it should be a boolean or None.
        If it's initialised from a Grid and it's None, the wrapping information of the copied grid is used.

    """

    def __init__(self, grid, y_is_down=None, wrapx=None, wrapy=None):
        if isinstance(grid, str):
            grid = readlines(grid)

        self.bounding_box = None

        if isinstance(grid, Grid):
            wrapx = grid.wrapx if wrapx == None else wrapx
            wrapy = grid.wrapy if wrapy == None else wrapy
            y_is_down = grid.y_is_down if y_is_down == None else y_is_down
            self.bounding_box = grid.bounding_box
            grid = grid.data

        wrapx = wrapx if wrapx != None else False
        wrapy = wrapy if wrapy != None else False

        if not type(wrapx) == bool:
            if not type(wrapx) == int:
                raise TypeError("wrapx must be a boolean, an integer, or None")
            if wrapx <= 0:
                raise Exception("wrapx must be positive")

        if not type(wrapy) == bool:
            if not type(wrapy) == int:
                raise TypeError("wrapy must be a boolean, an integer, or None")
            if wrapx <= 0:
                raise Exception("wrapy must be positive")

        self.wrapx = wrapx
        self.wrapy = wrapy
        self.y_is_down = y_is_down

        self.data = defaultdict(lambda: None)

        if isinstance(grid, list):
            if y_is_down == None:
                self.y_is_down = True
            elif not y_is_down:
                grid = reversed(grid)

            height = len(grid)

            widths = set(map(len, grid))
            if len(widths) != 1:
                print(
                    "WARNING: widths are not uniform. The maximum will be used.")
            width = max(widths)

            if width > 0 and height > 0:
                self.bounding_box = Rectangle((0, 0), (width-1, height-1))

            if wrapy:
                if type(wrapy) == int:
                    raise Exception(
                        "An explicit height may not be set when initialising from a list")
                self.wrapy = height
                if self.wrapy == 0:
                    raise Exception("Height may not be 0")

            if wrapx:
                if type(wrapx) == int:
                    raise Exception(
                        "An explicit width may not be set when initialising from a list")
                self.wrapx = width
                if self.wrapx == 0:
                    raise Exception("Width may not be 0")

            for (y, row) in enumerate(grid):
                if isinstance(row, str):
                    row = list(row)
                for (x, cell) in enumerate(row):
                    self.data[x, y] = cell

        elif isinstance(grid, dict):
            if y_is_down == None:
                self.y_is_down = False

            if wrapy == True:
                raise Exception(
                    "An explicit width must be set when initialising from a dict")
            if wrapx == True:
                raise Exception(
                    "An explicit height must be set when initialising from a dict")

            keys = dict.keys()
            for key in keys:
                elt = grid[key]
                (x, y) = convert_pos(key, True)
                if wrapx and x not in range(0, wrapx):
                    raise KeyError(
                        "x index must by in range [0,wrapx)", x, wrapx)
                if wrapy and y not in range(0, wrapy):
                    raise KeyError(
                        "y index must by in range [0,wrapy)", y, wrapy)
                self.data[x, y] = elt

            if self.bounding_box != None:
                # This only happens when we're copying another grid
                self._compute_bb()

        else:
            raise TypeError("Unsupported grid type", type(grid), grid)

    def _convert_pos1(self, key):
        """
        Converts the given external key to the type used internally; (x,y) tuples.
        Takes wrapping into account.
        """
        (x, y) = convert_pos(key, True)
        if self.wrapx:
            x %= self.wrapx
        if self.wrapy:
            x %= self.wrapy
        return (x, y)

    def _compute_bb(self):
        """
        Computes the bounding box of this grid.
        """
        self.bounding_box = bounding_box(self.keys(tuple))

    def __getitem__(self, key):
        return self.data[self._convert_pos1(key)]

    def __setitem__(self, key, value):
        key = self._convert_pos1(key)
        self.data[key] = value
        if value == None:
            return
        if self.bounding_box == None:
            self.bounding_box += key

    def keys(self, type=complex, include_nones=False):
        """
        Iterates over the keys of this grid.

        Arguments:
        - type: The type of keys to return. complex and tuple are supported.
        - include_nones: Whether to include keys that map to None.
            These may be spuriously created since it's backed by a defaultdict.
        """
        if type not in [complex, tuple]:
            raise Exception("Unsupported type", type)

        for key in self.data:
            if include_nones or self.data[key] != None:
                yield _pos_as(key, type)

    def __iter__(self):
        return self.keys()

    def __contains__(self, key):
        key = self._convert_pos1(key)
        return self._in_bb(key) and key in self.data

    def _in_bb(self, key):
        """
        Checks whetehr the given key is in the bounding box.
        """
        if self.bounding_box == None:
            return False
        return key in self.bounding_box

    def items(self, type=complex, include_nones=False):
        """
        Iterates over the keys and values of this grid.

        Arguments:
        - type: The type of keys to return. complex and tuple are supported.
        - include_nones: Whether to include keys that map to None.
            These may be spuriously created since it's backed by a defaultdict.
        """
        for key in self.keys(type, include_nones):
            yield (key, self[key])

    def width(self):
        """
        Returns the width of this grid.
        """
        if self.wrapx:
            return self.wrapx
        if self.bounding_box == None:
            return 0
        return self.bounding_box.width()

    def height(self):
        """
        Returns the height of this grid.
        """
        if self.wrapy:
            return self.wrapy
        if self.bounding_box == None:
            return 0
        return self.bounding_box.height()

    def draw(self, symbols=None, flipx=False, flipy=False):
        """
        Draws the grid to the screen.

        Arguments:
        - symbols: The mapping of values to characters to use.
            Can be a dict or a list.
            Defaults to mapping 0 to space and 1 to █.
            Any value not in symbols is converted to a string, and the first character is taken.
            Coordinates not in the grid are rendered as spaces.
        - flipx, flipy: Mirrors the rendering.
            The direction y is to be interpreted as is determined by self.y_is_down, which may then be flipped by flipy.
        """

        if symbols == None:
            symbols = {0: ' ', 1: '█'}

        if not isinstance(symbols, dict):
            symbols = {i: v for i, v in enumerate(symbols)}

        flipy ^= not self.y_is_down

        xrng = self.bounding_box.xrange()
        yrng = self.bounding_box.yrange()

        xrng = reversed(xrng) if flipx else xrng
        yrng = reversed(yrng) if flipy else yrng

        res = ''
        for y in yrng:
            for x in xrng:
                elt = self[x, y]
                if elt == None:
                    elt = ' '
                sym = symbols[elt] if elt in symbols else str(elt)[0]
                res += sym
            res += '\n'

        print(res)


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


def mint(x, default=None):
    """Maybe int - casts to int and returns default on failure"""
    try:
        return int(x)
    except ValueError:
        return default


def ints_in(x: str, positive=True):
    """Finds all integers in the string x"""
    ex = r'\d+' if positive else r'-?\d+'
    return ints(re.findall(ex, x))


def neighbours(p):
    """When p is a complex number with integer components, returns the four orthagonal neighbours of p."""
    return [p+1j**dir for dir in range(4)]


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


def bin_search(lo, hi, f):
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


def readlines(filename):
    """
    Returns the list of lines in the given file. Strips the trailing newline on each.
    """
    return mapl(lambda l: l[:-1], open(filename))


def irange(*args):
    """Inclusive range"""
    args = list(args)
    if len(args) == 1:
        args[0] += 1
    else:
        args[1] += 1
    return range(*args)


def submit(answer, part=1, day=None, year=2020, confirm=True):
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
