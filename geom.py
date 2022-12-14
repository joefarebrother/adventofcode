# pylint: disable=unsubscriptable-object # pylint bug in python 3.9
from typing import Optional, Iterable
import cmath
from misc_utils import irange, bounds, DotDict


class IVec2:
    """
    A 2d vector of integers. 
    Can be used like a complex number or a tuple.

    If strict is False, the constructor may return a complex number with non-integer parts.
    """

    __slots__ = "x", "y"
    _cache = {}

    def __new__(cls, x, y=None, strict=False):
        if isinstance(x, cls):
            return x
        if y is None and isinstance(x, list):
            x, y = x
        if (x, y) in cls._cache:
            return cls._cache[x, y]
        if y is None:
            if type(x) in (int, float, complex):
                x = complex(x)
                ix, iy = x.real, x.imag
                if not strict and not (ix == int(ix) and iy == int(iy)):
                    return x
            else:
                ix, iy = x
        else:
            ix, iy = x, y
        s = super(IVec2, cls).__new__(cls)
        assert ix == int(ix) and iy == int(iy), (ix, iy)
        s.x = int(ix)
        s.y = int(iy)
        cls._cache[x, y] = s
        return s

    @property
    def real(self) -> int:
        return self.x

    @property
    def imag(self) -> int:
        return self.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        try:
            other = IVec2(other)
        except (TypeError, ValueError):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)

    def __iter__(self):
        yield self.x
        yield self.y

    def __getitem__(self, idx):
        if idx == 0:
            return self.x
        if idx == 1:
            return self.y
        return NotImplemented

    def __repr__(self):
        return f"IVec2({self.x}, {self.y})"

    def __complex__(self):
        return self.x + 1j*self.y

    def __add__(self, other):
        if isinstance(other, complex):
            return IVec2(complex(self)+other)
        try:
            other = IVec2(other)
        except (TypeError, ValueError):
            return NotImplemented
        return IVec2(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        if isinstance(other, complex):
            return IVec2(complex(self)-other)
        try:
            other = IVec2(other)
        except (TypeError, ValueError):
            return NotImplemented
        return IVec2(self.x-other.x, self.y-other.y)

    __radd__ = __add__

    def __rsub__(self, other):
        if isinstance(other, complex):
            return IVec2(other-complex(self))
        try:
            other = IVec2(other)
        except (TypeError, ValueError):
            return NotImplemented
        return IVec2(other.x-self.x, other.y-self.y)

    def __mul__(self, other):
        if isinstance(other, complex):
            return IVec2(complex(self)*other)
        try:
            other = IVec2(other)
        except (TypeError, ValueError):
            return NotImplemented
        return IVec2(complex(self)*complex(other))

    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, complex):
            return IVec2(complex(self)/other)
        try:
            other = IVec2(other)
        except (TypeError, ValueError):
            return NotImplemented
        return IVec2(complex(self)/complex(other))

    def __rtruediv__(self, other):
        if isinstance(other, complex):
            return IVec2(other/complex(self))
        try:
            other = IVec2(other)
        except (TypeError, ValueError):
            return NotImplemented
        return IVec2(complex(other)/complex(self))

    def conjugate(self):
        return IVec2(self.x, -self.y)

    def abs(self) -> float:
        """Returns the Euclidean (L2) distance to the origin."""
        return abs(complex(self))

    __abs__ = abs

    def man_abs(self) -> int:
        """Returns the Manhattan (L1) distance to the origin."""
        return abs(self.x)+abs(self.y)

    def chess_abs(self) -> int:
        """Returns the Chessboard (Linf) distance to the origin; i.e. max(abs(x),abs(y)), the number of King moves to the origin."""
        return max(abs(self.x), abs(self.y))

    def angle(self) -> float:
        """Returns the angle as seen from the origin, in the range [0,tau). This is anticlockwise in the y-is-up convention."""
        ang = cmath.phase(complex(self))
        if ang < 0:
            ang += cmath.tau
        return ang

    def neighbours(self):
        """Returns the 4 orthogonal neighbours of self"""
        x, y = self.x, self.y
        return [IVec2(x+1, y), IVec2(x, y+1), IVec2(x-1, y), IVec2(x, y-1)]

    def neighbours8(self):
        """Returns the 8 neighbours of self"""
        x, y = self.x, self.y
        return [p for p in Rectangle((x-1, y-1), (x+1, y+1)) if p != self]


class Rectangle:
    """
    A rectangle with integer coordinates.

    Rectangle(*ps) is the bounding box of the given points. These points are inclusive.
    Rectangle() represents an empty rectangle.

    Supports addition of points and other rectangles.
    """

    def __init__(self, *ps):
        if len(ps) == 0:
            self.minx, self.maxx, self.miny, self.maxy = None, None, None, None
        else:
            if ps[0] is None:
                # internal optimisation
                (_, self.minx, self.miny, self.maxx, self.maxy) = ps
            else:
                ps = [IVec2(p, strict=True) for p in ps]
                xs = [p.x for p in ps]
                ys = [p.y for p in ps]

                self.minx, self.maxx = bounds(xs)
                self.miny, self.maxy = bounds(ys)

    def __bool__(self):
        return self.minx is not None

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

    def __len__(self) -> int:
        return self.width*self.height

    def xrange(self) -> range:
        """
        Returns the range of x-positions this rectangle spans.
        """
        return irange(self.minx, self.maxx) if self else range(0)

    def yrange(self) -> range:
        """
        Returns the range of y-positions this rectangle spans.
        """
        return irange(self.miny, self.maxy) if self else range(0)

    def points(self):
        """
        Yields the points of this rectangle, in increasing X values then increasing Y values.
        """
        for y in self.yrange():
            for x in self.xrange():
                yield IVec2(x, y)

    def expand_1(self):
        """
        Expands this rectangle by 1 unit in each direction.
        """
        return Rectangle(None, self.minx-1, self.miny-1, self.maxx+1, self.maxy+1)

    def __iter__(self):
        return self.points()

    def __contains__(self, other):
        try:
            if not self:
                return False
            z = IVec2(other, strict=True)
            return self.minx <= z.x <= self.maxx and self.miny <= z.y <= self.maxy
        except (TypeError, ValueError):
            return NotImplemented

    def __le__(self, other):
        if not isinstance(other, Rectangle):
            return NotImplemented
        return all(p in other for p in self.opposite_corners())

    def corners(self) -> list[IVec2]:
        """
        Returns the 4 corners of this rectangle. Order unspecified.
        """
        if not self:
            return []
        minx, miny, maxx, maxy = self.minx, self.miny, self.maxx, self.maxy
        return [IVec2(minx, miny), IVec2(minx, maxy), IVec2(maxx, maxy), IVec2(maxx, miny)]

    def opposite_corners(self) -> list[IVec2]:
        """
        Returns the 2 opposite corners with the min/max x/y positions.
        """
        if not self:
            return []
        minx, miny, maxx, maxy = self.minx, self.miny, self.maxx, self.maxy
        return [IVec2(minx, miny), IVec2(maxx, maxy)]

    def __add__(self, other):
        if isinstance(other, Rectangle):
            (p0, p1) = other.opposite_corners()
            return (self + p0) + p1
        else:
            try:
                other = IVec2(other)
            except (TypeError, ValueError):
                return NotImplemented
            if other in self:
                return self
            return bounding_box(self.opposite_corners() + [other])

    __radd__ = __add__

    def __repr__(self):
        return f"Rectangle{tuple(self.opposite_corners())}"

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
        return Rectangle()


def intersect_irange(r1: tuple, r2: tuple) -> Optional[tuple]:
    """
    Computes the intersection of the two given inclusive ranges, represented as tuples.
    Returns None if the intersection is empty.
    """
    (l1, h1) = r1
    (l2, h2) = r2
    upper = min(h1, h2)
    lower = max(l1, l2)
    if lower <= upper:
        return (lower, upper)
    else:
        return None


def bounding_box(points: Iterable) -> Rectangle:
    """
    Computes the bounding box of the given points.
    """
    return Rectangle(*points)


def neighbours(p) -> list[IVec2]:
    """
    Returns the 4 orthogonal neighbours of p.
    """
    return IVec2(p).neighbours()


def neighbours8(p) -> list[IVec2]:
    """
    Returns the 8 neighbors of p. 
    """
    return IVec2(p).neighbours8()


def dist(p1, p2=0) -> float:
    """
    Returns the Euclidean (L2) distance between the two specified points.
    Returns an integer if both inputs are integers.
    """
    if isinstance(p1, int) and isinstance(p2, int):
        return abs(p1-p2)
    return abs(IVec2(p1)-p2)


def man_dist(p1, p2=0) -> int:
    """
    Returns the Manhattan (L1) distance between the two specified points.
    """
    return (IVec2(p1)-p2).man_abs()


def chess_dist(p1, p2=0) -> int:
    """
    Returns the Chessboard (Linf) distance between the two specified points, i.e. the number of King moves between them.
    """
    return (IVec2(p1)-p2).chess_abs()


def angle(p0, p1=None) -> float:
    """
    angle(p0) returns the angle of p as seen from the origin. 
    angle(p0, p1) returns the angle of p1 as seen from p0.
    Returns a float in [0,tau); which is anticlockwise in the y-is-up convention and clockwise in the y-is-down convention.
    """
    if p1 is None:
        p = IVec2(p0)
    else:
        p = IVec2(p1) - IVec2(p0)
    return p.angle()


Dirs = DotDict()
Dirs.up = Dirs.U = Dirs.north = Dirs.N = IVec2(1j)
Dirs.down = Dirs.D = Dirs.south = Dirs.S = IVec2(-1j)
Dirs.left = Dirs.L = Dirs.west = Dirs.W = IVec2(-1+0j)
Dirs.right = Dirs.R = Dirs.east = Dirs.E = IVec2(1+0j)

Dirs.tL = 1j
Dirs.tR = -1j


def _flipy(d):
    def _dirs_flipy():
        for x in d:
            d[x] = d[x].conjugate()
    return _dirs_flipy


Dirs.flipy = _flipy(Dirs)

HexDirs = DotDict()
HexDirs.up = HexDirs.U = HexDirs.north = HexDirs.N = IVec2(2j)
HexDirs.down = HexDirs.D = HexDirs.south = HexDirs.S = IVec2(-2j)
HexDirs.left = HexDirs.L = HexDirs.west = HexDirs.W = IVec2(-2+0j)
HexDirs.right = HexDirs.R = HexDirs.east = HexDirs.E = IVec2(2+0j)
HexDirs.upleft = HexDirs.UL = HexDirs.northwest = HexDirs.NW = IVec2(-1+1j)
HexDirs.upright = HexDirs.UR = HexDirs.northeast = HexDirs.NE = IVec2(1+1j)
HexDirs.downleft = HexDirs.DL = HexDirs.southwest = HexDirs.SW = IVec2(-1-1j)
HexDirs.downright = HexDirs.DR = HexDirs.southeast = HexDirs.SW = IVec2(+1+1j)

HexDirs.flipy = _flipy(HexDirs)
