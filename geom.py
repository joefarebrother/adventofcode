# pylint: disable=unsubscriptable-object # pylint bug in python 3.9
from typing import Optional, Iterable
import cmath, math, itertools
from misc_utils import irange, bounds, DotDict, modify_idx


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
        raise ValueError("Bad index for point:", self, idx)

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

    def __neg__(self):
        return IVec2(-self.x, -self.y)

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
        return self.width()*self.height()

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

    def difference(self, other):
        """Returns a list of non-overlapping rectangles whose union is the difference between self and other"""
        res = []
        if not self & other:
            return [self]

        locur = [self.minx, self.miny]
        hicur = [self.maxx, self.maxy]

        for d, (c0, c1, o0, o1) in enumerate(zip(locur, hicur, [other.minx, other.miny], [other.maxx, other.maxy], strict=True)):
            #       oooooooooooooo              oooooooooooooo
            #       o            o              o            o
            #  ccccccccccc       o         rrrrrcccccc       o
            #  c    o    c       o         r   rc    c       o
            #  c    o    c       o         r   rc    c       o
            #  c    ooooocoooooooo    =>   r   rcoooocoooooooo
            #  c         c                 r   rc    c
            #  c         c                 r   rc    c
            #  c         c                 r   rc    c
            #  c         c                 r   rc    c
            #  c         c                 r   rc    c
            #  ccccccccccc                 rrrrrcccccc
            #

            # left
            if c0 < o0 <= c1:
                res.append((tuple(locur), modify_idx(tuple(hicur), d, o0-1)))
                locur[d] = o0
            # right
            if c0 <= o1 < c1:
                res.append((modify_idx(tuple(locur), d, o1+1), tuple(hicur)))
                hicur[d] = o1

        res2 = []
        for (rlo, rhi) in res:
            res2.append(Rectangle(rlo, rhi))

        return res2


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

class Interval:
    """
    An interval.
    """
    def __init__(self, start, end=None, len=None, inclusive=True, sort=False): #pylint:disable=redefined-builtin # len is really the best name for this
        if end is None and len is None:
            start,end = start 
        elif end is None and len is not None:
            end = start+len
            inclusive=False 
        elif end is not None and len is not None:
            raise Exception("Cannot specify both end and len:", start, end, len)
        
        if sort:
            if not inclusive:
                raise Exception("Can only sort inclusive ranges")
            start,end = sorted((start,end))

        if inclusive:
            end += 1
        
        assert end >= start

        if start == end:
            start = end = 0

        self._start = start
        self._end = end 

    @property
    def start(self):
        """Gets the start point of this interval"""
        return self._start
    
    @property
    def endi(self):
        """Gets the inclusive endpoint of this interval"""
        return self._end-1 
    
    @property
    def endx(self):
        """Gets the exclusive endpoint of this interval"""
        return self._end 
    
    @property
    def len(self):
        """Returns the length of this interval"""
        return self.endx-self.start 
    
    @property
    def tupi(self):
        """Returns this interval as an inclusive tuple"""
        return self.start, self.endi 
    
    @property
    def tupx(self):
        """Returns this interval as an exclusive tuple"""
        return self.start, self.endx
                

    def __eq__(self, other):
        if isinstance(other, Interval):
            return self.tupx == other.tupx
        if isinstance(other, tuple):
            return self.tupi == other 
        return NotImplemented 
    
    def __hash__(self):
        return hash(self.tupi)
    
    def __and__(self, other):
        if isinstance(other,Interval):
            other = other.tupi
        if not isinstance(other, tuple):
            return NotImplemented
        
        res = intersect_irange(self.tupi, other)
        if res is None:
            return Interval(0, len=0)
        return Interval(res)
    
    __rand__ = __and__
    
    @property
    def range(self):
        return range(self.start, self.endx)
    
    def __contains__(self, pt):
        return self.start <= pt < self.endx
    
    def __repr__(self):
        return f"Interval({self.start}, {self.endi})"
    
    def complement(self):
        """Returns the complement of this interval, as an `IntervalSet`"""
        return IntervalSet([self]).complement()
    
    def shift(self, amt):
        """Returns this interval shifted by `amt`"""
        return Interval(self.start+amt, self.endx+amt, inclusive=False)
    
    def __bool__(self):
        return bool(self.len)
    
class IntervalSet:
    """A set of integers, represented as a collection of disjoint intervals"""
    def __init__(self, parts=None):
        if parts is None:
            parts = []
        if isinstance(parts,Interval) or (isinstance(parts,tuple) and isinstance(parts[0],int)):
            parts = [parts]
        ps = []
        for p in parts:
            if isinstance(p, Interval):
                if not p:
                    continue
                p = p.tupi 
            ps = IntervalSet._add_interval(ps, p)
        self._parts = ps 

    @staticmethod
    def _add_interval(intervals, interval):
        # invariant: intervals is a list of disjoint, non-adjacent, inclusive intervals sorted by their lowest endpoint
        n_int = []
        x0, x1 = interval
        if x1-x0 == -1:
            return intervals
        assert x0 <= x1, (x0,x1)
        i = 0
        # binary search isn't more efficient as slicing the list is linear anyway
        while i < len(intervals):
            y0, y1 = intervals[i]
            if y1+1 < x0:
                n_int.append((y0, y1))
            elif x1+1 < y0:
                break
            else:
                x0 = min(x0, y0)
                x1 = max(x1, y1)
            i += 1
        n_int.append((x0, x1))
        n_int += intervals[i:]
        return n_int
    
    @classmethod 
    def _new(cls, parts):
        res = cls.__new__(cls)
        res._parts = parts #pylint:disable=protected-access # TODO: is there a way to do a sort of private constructor that doesn't require disabling this lint?
        return res

    def __or__(self, other):
        if isinstance(other,IntervalSet):
            ops = other._parts
        elif isinstance(other, Interval):
            ops = [other.tupi]*bool(other)
        elif isinstance(other,tuple):
            ops = [other]
        else:
            return NotImplemented
        
        ps = self._parts 
        for p in ops:
            ps = IntervalSet._add_interval(ps, p)

        return IntervalSet._new(ps)
    
    __ror__ = __or__
    
    def __and__(self, other):
        if isinstance(other,IntervalSet):
            ops = other._parts
        elif isinstance(other, Interval):
            ops = [other.tupi]*bool(other)
        elif isinstance(other,tuple):
            ops = [other]
        else:
            return NotImplemented
        
        sps = self._parts 

        nps = []
        try:
            ops = iter(ops)
            sps = iter(sps)

            csp = next(sps)
            cop = next(ops)

            while True:
                r = intersect_irange(csp,cop)
                if r is not None:
                    nps.append(r)
                if csp[1]<cop[1]:
                    csp = next(sps)
                else:
                    cop = next(ops)

        except StopIteration:
            return IntervalSet._new(nps)
        
    __rand__ = __and__

    def complement(self):
        """Returns the complement of this set"""
        nps = []
        prev = -math.inf
        for (lo,hi) in self._parts:
            cinv = (prev,lo-1)
            if lo != -math.inf:
                nps.append(cinv)
            prev = hi+1 
        if prev != math.inf:
            nps.append((prev,math.inf))

        return IntervalSet._new(nps)

    def __sub__(self, other):
        if isinstance(other,IntervalSet):
            pass
        elif isinstance(other, Interval):
            other = IntervalSet([other])
        elif isinstance(other,tuple):
            other = IntervalSet([other])
        else:
            return NotImplemented
        
        return self & other.complement()
    
    def __rsub__(self, other):
        return self.complement() & other
    
    def shift(self, amt):
        """Returns this interval shifted by `amt`"""
        return IntervalSet._new([(l+amt,h+amt) for l,h in self._parts])
    
    @property
    def intervals(self):
        """Gets the list of intervals representing this set"""
        return [Interval(lo,hi) for lo,hi in self._parts]
    
    def len(self):
        """Returns the length of this set"""
        return sum(hi-lo+1 for hi,lo in self._parts)

    def __bool__(self):
        return bool(self.len())
    
    def __contains__(self, elem):
        # TODO: binary search 
        for lo,hi in self._parts:
            if lo <= elem <= hi:
                return True 
            if elem < lo:
                return False 
        return False
    
    def __eq__(self, other):
        if isinstance(other, IntervalSet):
            return self._parts == other._parts 
        return NotImplemented
    
    def __hash__(self):
        return hash(tuple(self._parts))
    
    def __repr__(self):
        return f"IntervalSet({self._parts})"
    
class Cuboid:
    """An n-dimensional hypercuboid"""

    def __init__(self, dims):
        if isinstance(dims, Rectangle):
            dims = [(dims.minx,dims.maxx),(dims.miny,dims.maxy)]
        self.dims = []
        zero = False
        for d in dims:
            if not isinstance(d, Interval):
                d = Interval(d,sort=True)
            if d.len == 0:
                zero = True
            self.dims.append(d)

        if zero:
            self.dims = [Interval(0,len=0)]*len(self.dims)
        self.dims = tuple(self.dims)

    def volume(self):
        return math.prod(d.len for d in self.dims)
    
    def as_rect(self):
        assert len(self.dims) == 2
        if not self.volume():
            return None
        (minx,maxx),(miny,maxy) = self.dims[0].tupi,self.dims[1].tupi 
        return Rectangle((minx,miny),(maxx,maxy))
    
    def __and__(self, other):
        if isinstance(other,Rectangle):
            other = Cuboid(other)
        if not isinstance(other,Cuboid):
            return NotImplemented
        
        return Cuboid(a & b for a,b in zip(self.dims,other.dims,strict=True))

    __rand__ = __and__

    def __bool__(self):
        return bool(self.volume())
    
    def difference_list(self,other):
        if not isinstance(other,Cuboid):
            return NotImplemented
        
        if not (self & other):
            return [self]
        
        sdims = list(self.dims)
        res = []
        for i,(saxis,oaxis) in enumerate(zip(self.dims,other.dims,strict=True)):
            diff = IntervalSet(saxis)-oaxis 
            inter = saxis & oaxis 

            #             oooooooooooooooo                    oooooooooooooooo
            #             o              o                    o              o
            #  cccccccccccccccccccccccc  o         rrrrrrrrrrrccccccccccccc  o
            #  c          o           c  o         r         rc           c  o
            #  c <-diff-> o           c  o         r <-diff->rc           c  o
            #  c          ooooocoooooooooo    =>   r         rcoooocoooooooooo
            #  c                      c            r         rc           c
            #  c           <-inter->  c            r         rc<-inter->  c
            #  c                      c            r         rc           c
            #  c                      c            r         rc           c
            #  c                      c            r         rc           c
            #  cccccccccccccccccccccccc            rrrrrrrrrrrccccccccccccc
            #

            for diffi in diff.intervals:
                sdims[i] = diffi 
                assert diffi.len > 0, diffi
                res.append(Cuboid(sdims))

            sdims[i] = inter
            if inter.len == 0:
                break

        assert all(c.volume()>0 for c in res), res
        return res
    
    def __eq__(self,other):
        if not isinstance(other,Cuboid):
            return NotImplemented
        return self.dims == other.dims 

    def __hash__(self):
        return hash(self.dims)
    
    def __repr__(self):
        return f"Cuboid({list(self.dims)})"
    
    def complement(self):
        """Returns the complement of this cuboid as a cuboid set"""
        return CuboidSet([self]).complement()
    
def infinite_cuboid(ndims):
    """Returns the cuboid representing the entire n-dimensional space"""
    return Cuboid([(-math.inf,math.inf)]*ndims)

def hyperplane(axis,ndims,val,symbol):
    """Returns the hyperplane or hyper half-space for which the given axis is related to the given value by `symbol` (<,<=,=,=>,>)"""
    dims = [(-math.inf,math.inf)]*ndims
    match symbol:
        case "<": dim = Interval(-math.inf,val,inclusive=False)
        case "<=": dim = Interval(-math.inf,val,inclusive=True)
        case ">": dim = Interval(val+1,math.inf)
        case ">=": dim = Interval(val,math.inf)
        case "=": dim = Interval(val,val,inclusive=True)

    dims[axis] = dim

    return Cuboid(dims)

class CuboidSet:
    """A set of points in n-dimensional space represented, as a collection of disjoint cuboids"""

    def __init__(self, cubs=None):
        if cubs==None:
            cubs = []
        if isinstance(cubs,Cuboid) or isinstance(cubs,Rectangle):
            cubs = [cubs]

        ncubs = []
        for c in cubs:
            if isinstance(c,Rectangle):
                c = Cuboid(c)
            ncubs = CuboidSet.add_cuboid(ncubs,c)

        self.cubs = frozenset(ncubs)

    def volume(self):
        """Computes the volume of this set"""
        return sum(c.volume() for c in self.cubs)

    @classmethod
    def _new(cls,cubs):
        res = cls.__new__(cls)
        res.cubs = frozenset(cubs)
        assert all(c.volume()>0 for c in cubs)
        return res

    @staticmethod
    def add_cuboid(cubs,cub):
        if cub.volume() == 0:
            return cubs
        res = [cub]
        for c in cubs:
            res += c.difference_list(cub)
        return res

    def __or__(self,other):
        if isinstance(other,Rectangle):
            ocubs = [Cuboid(other)]
        elif isinstance(other,Cuboid):
            ocubs = [other]
        elif isinstance(other,CuboidSet):
            ocubs = other.cubs
        else:
            return NotImplemented 
        
        ncubs = self.cubs
        for c in ocubs:
            ncubs = CuboidSet.add_cuboid(ncubs,c)
        return CuboidSet._new(ncubs)
    
    __ror__ = __or__

    def __and__(self,other):
        if isinstance(other,Rectangle):
            ocubs = [Cuboid(other)]
        elif isinstance(other,Cuboid):
            ocubs = [other]
        elif isinstance(other,CuboidSet):
            ocubs = other.cubs
        else:
            return NotImplemented

        ncubs = []
        for a,b in itertools.product(self.cubs,ocubs):
            c = a & b 
            if c.volume() > 0:
                ncubs.append(c)

        return CuboidSet._new(ncubs)
    
    __rand__ = __and__

    def __sub__(self,other):
        if isinstance(other,Rectangle):
            ocubs = [Cuboid(other)]
        elif isinstance(other,Cuboid):
            ocubs = [other]
        elif isinstance(other,CuboidSet):
            ocubs = other.cubs
        else:
            return NotImplemented 
        
        def dif_one(cubs,c):
            ncubs = []
            for cc in cubs:
                ncubs += cc.difference_list(c)
            return ncubs

        cubs = self.cubs 
        for c in ocubs:
            cubs = dif_one(cubs,c)

        return CuboidSet._new(cubs)
    
    def __rsub__(self,other):
        if isinstance(other,Rectangle):
            ocubs = [Cuboid(other)]
        elif isinstance(other,Cuboid):
            ocubs = [other]
        elif isinstance(other,CuboidSet):
            ocubs = other.cubs
        else:
            return NotImplemented 
        
        return CuboidSet._new(ocubs) - self

    def __eq__(self,other):
        if not isinstance(other,CuboidSet):
            return NotImplemented 
        return self.cubs == other.cubs 

    def __hash__(self):
        return hash(self.cubs)

    def __repr__(self):
        return f"CuboidSet({list(self.cubs)})"

    def complement(self):
        """Returns the complement of this set"""
        if not self.cubs:
            raise Exception("Cannot determine dimension")
        return CuboidSet._new([infinite_cuboid(len(next(iter(self.cubs)).dims))])        

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
Dirs.up = Dirs.U = Dirs.north = Dirs.N = Dirs["^"] = IVec2(1j)
Dirs.down = Dirs.D = Dirs.south = Dirs.S = Dirs["v"] = IVec2(-1j)
Dirs.left = Dirs.L = Dirs.west = Dirs.W = Dirs["<"] = IVec2(-1+0j)
Dirs.right = Dirs.R = Dirs.east = Dirs.E = Dirs[">"] = IVec2(1+0j)

Dirs.tL = 1j
Dirs.tR = -1j


def _flipy(d):
    def _dirs_flipy():
        for x in d:
            if hasattr(d[x], "conjugate"):
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
