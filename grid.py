from collections import Counter
from typing import Callable
from geom import Rectangle, bounding_box, is_pos_ty, pos_as
from input_utils import inp_readlines
from collections.abc import MutableMapping


class Grid(MutableMapping):
    """
    A grid that can be indexed by positions.

    Constructor arguments:
    - grid: Determines the initial data.
        Can be a another Grid, a list (of rows which are lists or strings), or a dict (with keys being positions)
        Data is copies and isn't aliased.
        Can also be a string, which will be treated as a filenane, where the lines will be rows; or an integer, which uses the input file for that day.
    - default: Default value for empty cells. 
        Should be immutable else it may lead to bugs as the same reference would be used for each. 
    - y_is_down: Whether a higher y index is to be interpreted as down.
        The default is determined by the type of grid: If it's a list/file, it's True, if it's a dict its False, and if its' a Grid it's copied.
        If it's set to False when its a list, the the top-left corner will still be (0,0), so it will be negative for subsequent rows.
        Otherwise, it only matters for printing.
    - wrapx, wrapy: Determines whether to wrap in the given direction, making the grid into a cylinder or torus.
        Grid indicies must be in the range [0, width/height)
        If data is initialised from a dict or another Grid, this should be a positive integer, False, or None. An integer represents an explicit width/height.
        If it's initialised from a list, it should be a boolean or None.
        If it's initialised from a Grid and it's None, the wrapping information of the copied grid is used.
    - ints: whether to cast the given data to ints
    - keyty: The position type of keys to return from iteration. Can be complex or tuple.
    """

    def __init__(self, grid=None, default=None, y_is_down=None, ints=False, wrapx=None, wrapy=None, keyty=complex):
        if isinstance(grid, str) or isinstance(grid, int):
            grid = inp_readlines()

        if grid == None:
            grid = {}

        self.bounding_box = None
        self.keyty(keyty)

        if isinstance(grid, Grid):
            wrapx = grid.wrapx if wrapx == None else wrapx
            wrapy = grid.wrapy if wrapy == None else wrapy
            y_is_down = grid.y_is_down if y_is_down == None else y_is_down
            default = grid.default if default == None else default
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

        self.data = {}
        self.default = default

        if isinstance(grid, list):
            if self.y_is_down == None:
                self.y_is_down = True

            if wrapy:
                if type(wrapy) == int:
                    raise Exception(
                        "An explicit height may not be set when initialising from a list")
                height = len(grid)
                self.wrapy = height
                if height == 0:
                    raise Exception("Height may not be 0")

            if wrapx:
                if type(wrapx) == int:
                    raise Exception(
                        "An explicit width may not be set when initialising from a list")
                widths = set(map(len, grid))
                if len(widths) != 1:
                    print(
                        "WARNING: widths are not uniform. The maximum will be used.")
                width = max(widths)

                self.wrapx = width
                if width == 0:
                    raise Exception("Width may not be 0")

            for (y, row) in enumerate(grid):
                y = y if self.y_is_down else -y
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

            keys = grid.keys()
            for key in keys:
                elt = grid[key]
                (x, y) = pos_as(tuple, key, True)
                if wrapx and x not in range(0, wrapx):
                    raise KeyError(
                        "x index must by in range [0,wrapx)", x, wrapx)
                if wrapy and y not in range(0, wrapy):
                    raise KeyError(
                        "y index must by in range [0,wrapy)", y, wrapy)
                self.data[x, y] = elt

        else:
            raise TypeError("Unsupported grid type", type(grid), grid)

        self._compute_bb()

        if ints:
            for p in self.data:
                self.data[p] = int(self.data[p])

    def _convert_pos1(self, key):
        """
        Converts the given external key to the type used internally; (x,y) tuples.
        Takes wrapping into account.
        """
        (x, y) = pos_as(tuple, key, True)
        if self.wrapx:
            x %= self.wrapx
        if self.wrapy:
            x %= self.wrapy
        return (x, y)

    def keyty(self, ty):
        """
        Sets the position type of keys to return when iterating, and then returns self.
        type should be complex or tuple.
        """
        if not is_pos_ty(ty):
            raise ValueError("Invalid position type", ty)
        self._keyty = ty
        return self

    def _compute_bb(self):
        """
        Computes the bounding box of this grid.
        """
        self.bounding_box = bounding_box(self.data.keys())

    def __getitem__(self, key):
        key = self._convert_pos1(key)
        return self.data[key] if key in self.data else self.default

    def __setitem__(self, key, value):
        key = self._convert_pos1(key)
        self.data[key] = value
        self.bounding_box += key

    def __delitem__(self, key):
        key = self._convert_pos1(key)
        del self.data[key]
        self._compute_bb()

    def __iter__(self):
        for key in self.data:
            yield pos_as(self._keyty, key)

    def __contains__(self, key):
        key = self._convert_pos1(key)
        return key in self.data

    def __len__(self):
        return len(self.data)

    def width(self) -> int:
        """
        Returns the width of this grid.
        """
        if self.wrapx:
            return self.wrapx
        return self.bounding_box.width()

    def height(self) -> int:
        """
        Returns the height of this grid.
        """
        if self.wrapy:
            return self.wrapy
        return self.bounding_box.height()

    def map(self, f: Callable):
        """
        Applies f to each element of the grid.
        """
        res = Grid(self)
        for p, v in self.data.items():
            res[p] = f(v)
        return res

    def count(self, x):
        """
        Counts the number of occurences of `x` in the grid.
        If `x` is he default item, points not in the grid's backing map are ignored.
        """
        c = 0
        for v in self.data.values():
            if v == x:
                c += 1
        return c

    def counter(self):
        """
        Returns a `Counter` counting the number of occurances of each element of the grid.
        """
        return Counter(self.data.values())

    def draw(self, symbols=None, flipx=False, flipy=False) -> None:
        """
        Draws the grid to the screen.

        Arguments:
        - symbols: The mapping of values to characters to use.
            Can be a dict or a list.
            If the grid consists entirely of 0 and 1, defaults to mapping 0 to space and 1 to █.
            Similarly if the grid consists entirely of . and #.
            If the grid consists entirely of a single entry, defaults to mapping that to █.
            Any value not in symbols is converted to a string, and the first character is taken.
            Coordinates not in the grid are rendered as spaces.
        - flipx, flipy: Mirrors the rendering.
            The direction y is to be interpreted as is determined by self.y_is_down, which may then be flipped by flipy.
        """

        if symbols == None:
            v = set(self.values())
            if len(v) <= 2 and v <= {0, 1, "0", "1", "#", "."}:
                symbols = {0: ' ', 1: '█', "0": " ",
                           "1": '█', ".": " ", "#": '█'}
            elif len(v) == 1:
                symbols = {list(v)[0]: '█'}
            else:
                symbols = {}

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
