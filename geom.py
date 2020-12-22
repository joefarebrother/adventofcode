# pylint: disable=unsubscriptable-object # pylint bug in python 3.9
from typing import Optional, Iterable, NewType, Union
import cmath
import itertools
from attrdict import AttrDict
from misc_utils import irange, bounds

Position = NewType('Position', Union[complex, tuple])


class Rectangle:
    """
    A rectangle.

    Rectangle(*ps) is the bounding box of the given points. These points are inclusive.
    If ints is True, all coordinates will be converted to ints.
    Rectangle() represents an empty rectangle.

    Supports addition of points and other rectangles.
    """

    def __init__(self, *ps: Position, ints=True):
        if len(ps) == 0:
            self.minx, self.maxx, self.miny, self.maxy = None, None, None, None
        else:
            if ps[0] == None:
                # internal optimisation
                (_, self.minx, self.miny, self.maxx, self.maxy) = ps
            else:
                ps = [pos_as(tuple, p, ints) for p in ps]
                xs = [x for (x, y) in ps]
                ys = [y for (x, y) in ps]

                self.minx, self.maxx = bounds(xs)
                self.miny, self.maxy = bounds(ys)

    def __bool__(self):
        return self.minx != None

    def width(self) -> int:
        """
        Returns the width of this rectangle.
        """
        return self.maxx-self.minx+1 if self else 0

    def height(self) -> int:
        """
        Returns the height of this rectangle.
        """
        return self.maxy-self.miny+1 if self else 0

    def xrange(self) -> range:
        """
        Returns the range of x-positions this rectangle spans.
        Only valid if the coordinates are integers.
        """
        return irange(self.minx, self.maxx) if self else range(0)

    def yrange(self) -> range:
        """
        Returns the range of y-positions this rectangle spans.
        Only valid if the coordinates are integers.
        """
        return irange(self.miny, self.maxy) if self else range(0)

    def points(self, ty=complex):
        for x in self.xrange():
            for y in self.yrange():
                yield pos_as(ty, (x, y))

    def __iter__(self):
        return self.points()

    def __contains__(self, other):
        if is_pos(other):
            if not self:
                return False
            (x, y) = pos_as(tuple, other)
            return self.minx <= x <= self.maxx and self.miny <= y <= self.maxy
        return NotImplemented

    def __le__(self, other):
        if not isinstance(other, Rectangle):
            return NotImplemented
        return all([p in other for p in self.opposite_corners()])

    def corners(self, ty=complex) -> list[Position]:
        """
        Returns the 4 corners of this rectangle, as positions of the given type. Order unspecified.
        """
        if not self:
            return []
        minx, miny, maxx, maxy = self.minx, self.miny, self.maxx, self.maxy
        corners = [(minx, miny), (minx, maxy), (maxx, maxy), (maxx, miny)]
        return [pos_as(ty, p) for p in corners]

    def opposite_corners(self, ty=complex) -> list[Position]:
        """
        Returns the 2 opposite corners with the min/max x/y positions.
        """
        if not self:
            return []
        minx, miny, maxx, maxy = self.minx, self.miny, self.maxx, self.maxy
        corners = [(minx, miny), (maxx, maxy)]
        return [pos_as(ty, p) for p in corners]

    def __add__(self, other):
        if isinstance(other, Rectangle):
            (p0, p1) = other.opposite_corners()
            return (self + p0) + p1
        elif is_pos(other):
            if other in self:
                return self
            return bounding_box(self.opposite_corners(tuple) + [other])
        else:
            return NotImplemented

    __radd__ = __add__

    def __repr__(self):
        return f"Rectangle{tuple(self.opposite_corners(tuple))}"

    def __eq__(self, other):
        if not isinstance(other, Rectangle):
            return NotImplemented
        return (self.minx, self.maxx, self.miny, self.maxy) == (other.minx, other.maxx, other.miny, other.maxy)

    def __hash__(self):
        return hash((self.minx, self.maxx, self.miny, self.maxy))

    def __and__(self, other):
        if not isinstance(other, Rectangle):
            return NotImplemented

        if not (self and other):
            return Rectangle()

        xint = intersect_irange((self.minx, self.maxx),
                                (other.minx, other.maxx))
        yint = intersect_irange((self.miny, self.maxy),
                                (other.miny, other.maxy))

        if xint and yint:
            (minx, maxx) = xint
            (miny, maxy) = yint
            return Rectangle(None, minx, miny, maxx, maxy)


def intersect_irange(r1: tuple, r2: tuple) -> Optional[tuple]:
    """
    Computes the intersection of the two given inclusive ranges, represented as tuples.
    Returns None if the intersection is empty.
    Actual range objects aren't used because they can't contain floats.
    """
    (l1, h1) = r1
    (l2, h2) = r2
    upper = min(h1, h2)
    lower = max(l1, l2)
    if lower <= upper:
        return (lower, upper)
    else:
        return None


def bounding_box(points: Iterable[Position]) -> Rectangle:
    """
    Computes the bounding box of the given points.
    """
    return Rectangle(*points)


def is_pos(pos) -> bool:
    """
    Checks whether pos is a 2D position. Can be a complex number or a 2-tuple.
    """
    if isinstance(pos, complex):
        return True
    if isinstance(pos, tuple):
        return len(pos) == 2
    return False


def is_pos_ty(ty) -> bool:
    """
    Checks whether ty is a type that can represent a 2d position, i.e. complex or tuple.
    """
    return ty in [complex, tuple]


def pos_as(ty, pos: Position, ints=False):
    """
    Converts the given position to the given type. Supported types are complex and tuple.
    ints determines whther to cast complex coords to ints.
    """
    if pos == 0:
        pos = 0j
    if ty == type(pos):
        return pos
    elif ty == tuple:
        if type(pos) != complex:
            raise TypeError("Expected a position (2-tuple or complex)")
        tup = (pos.real, pos.imag)
        return tuple(map(int, tup)) if ints else tup
    elif ty == complex:
        if type(pos) != tuple or len(pos) != 2:
            raise TypeError("Expected a position (2-tuple or complex)")
        (x, y) = pos
        return x + y*1j
    else:
        raise ValueError("Unsupported position type", type)


def neighbours(p: Position) -> list[complex]:
    """
    Returns the 4 orthoganal neighbours of p.
    """
    if p == 0:
        p = 0j
    p = pos_as(complex, p)
    return [p+1j**dir for dir in range(4)]


def neighbours8(p: Position) -> list[complex]:
    """
    Returns the 8 neighbors of p. 
    """
    z = pos_as(complex, p)
    return [z+d for d in Rectangle(-1-1j, 1+1j) if d != 0j]


def dist(p1: Position, p2: Position = 0j) -> float:
    """
    Returns the Euclidian distance between the two specified points.
    """
    return abs(pos_as(complex, p1), pos_as(complex, p2))


def man_dist(p1: Position, p2: Position = 0j, toint=True) -> float:
    """
    Returns the manhatten distance between the two specified points.
    Converts to an integer if toint is set.
    """
    diff = pos_as(complex, p1) - pos_as(complex, p2)
    dist = abs(diff.real) + abs(diff.imag)
    return int(dist) if toint else dist


def angle(p0: Position, p1=None) -> float:
    """
    angle(p0) returns the angle of p as seen from the origin. 
    angle(p0, p1) returns the angle of p1 as seen from p0.
    Returns a float in [0,tau); which is anticlockwise in the y-is-up convention and clockwise in the y-is-down convention.
    """
    if p1 == None:
        p = pos_as(complex, p)
    else:
        p = pos_as(complex, p1) - pos_as(complex, p0)
    ang = cmath.phase(p)  # range [-pi, pi]
    if ang < 0:
        ang += cmath.tau
    return ang


Dirs = AttrDict()
Dirs.up = Dirs.U = Dirs.north = Dirs.N = 1j
Dirs.down = Dirs.D = Dirs.south = Dirs.S = -1j
Dirs.left = Dirs.L = Dirs.west = Dirs.W = -1+0j
Dirs.right = Dirs.R = Dirs.east = Dirs.E = 1+0j

Dirs.tL = 1j
Dirs.tR = -1j
