from typing import Optional, Iterable, List, NewType, Union

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
            self.minx, self.mixx, self.miny, self.maxy = None, None, None, None
        else:
            if ps[0] == None:
                # internal optimisation
                (_, self.minx, self.miny, self.maxx, self.maxy) = ps
            else:
                ps = [convert_pos(p, ints) for p in ps]
                xs = [x for (x, y) in ps]
                ys = [y for (x, y) in ps]

                self.minx, self.maxx = min(xs), max(xs)
                self.miny, self.maxy = min(ys), max(ys)

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
        return range(self.minx, self.maxx+1) if self else range(0)

    def yrange(self) -> range:
        """
        Returns the range of y-positions this rectangle spans.
        Only valid if the coordinates are integers.
        """
        return range(self.miny, self.maxy+1) if self else range(0)

    def __contains__(self, other):
        if is_pos(other):
            if not self:
                return False
            (x, y) = convert_pos(other)
            return self.minx <= x <= self.maxx and self.miny <= y <= self.maxy
        return NotImplemented

    def __le__(self, other):
        if not isinstance(other, Rectangle):
            return NotImplemented
        return all([p in other for p in self.opposite_corners()])

    def corners(self, type=complex) -> List[Position]:
        """
        Returns the 4 corners of this rectangle, as positions of the given type. Order unspecified.
        """
        if not self:
            return []
        minx, miny, maxx, maxy = self.minx, self.miny, self.maxx, self.maxy
        corners = [(minx, miny), (minx, maxy), (maxx, maxy), (maxx, miny)]
        if type == tuple:
            return corners
        else:
            return [_pos_as(p, type) for p in corners]

    def opposite_corners(self, type=complex) -> List[Position]:
        """
        Returns the 2 opposite corners with the min/max x/y positions.
        """
        if not self:
            return []
        minx, miny, maxx, maxy = self.minx, self.miny, self.maxx, self.maxy
        corners = [(minx, miny), (maxx, maxy)]
        if type == tuple:
            return corners
        else:
            return [_pos_as(p, type) for p in corners]

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


def bounding_box(points: Iterable) -> Rectangle:
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
    if isinstance(pos, (tuple, list)):
        return len(pos) == 2
    return False


def is_pos_ty(ty) -> bool:
    """
    Checks whether ty is a type that can represent a 2d position., i.e. complex or tuple.
    """
    return ty in [complex, tuple]


def convert_pos(pos: Position, ints=True) -> tuple:
    """
    Converts the given position to the type used internally; (x,y) tuples.
    Supported position types are complex numbers, and length 2 tuples/lists.
    """
    if not is_pos(pos):
        raise TypeError("Expected a position", type(pos), pos)

    if isinstance(pos, complex):
        pos = (pos.real, pos.imag)
    return tuple(map(int, pos)) if ints else tuple(pos)


def _pos_as(pos: tuple, type):
    """
    Converts the given position from an (x,y) tuple to the given type. Supported types are complex and tuple.
    """
    if type == tuple:
        return pos
    elif type == complex:
        (x, y) = pos
        return x + y*1j
    else:
        raise Exception("Unsupported position type", type)


def neighbours(p: Position) -> List[Position]:
    """
    Returns the 4 orthoganal neighbours of p.
    """
    if isinstance(p, complex) or p == 0:
        return [p+1j**dir for dir in range(4)]
    else:
        (x, y) = p
        return [(x+1, y), (x, y+1), (x-1, y), (x, y-1)]
