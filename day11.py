# pylint: disable=unused-wildcard-import
from utils import *

grid = Grid("11.in")


def evolve1(grid):
    ngrid = Grid(grid)
    for (k, v) in grid.items():
        if v == ".":
            pass
        elif v == "L":
            if count_n(k, grid) == 0:
                ngrid[k] = "#"
        elif v == "#":
            if count_n(k, grid) >= 4:
                ngrid[k] = "L"
    return ngrid

    # If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
    # If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
    # Otherwise, the seat's state does not change.


def count_n(k, grid):
    count = 0
    for dx in irange(-1, 1):
        for dy in irange(-1, 1):
            if dx or dy:
                count += int(grid[k + dx + dy*1j] == "#")
    return count


def count_o(grid):
    return list(grid.values()).count("#")


def evolve2(grid):
    ngrid = Grid(grid)
    for (k, v) in grid.items():
        if v == ".":
            pass
        elif v == "L":
            if count_seen(k, grid) == 0:
                ngrid[k] = "#"
        elif v == "#":
            if count_seen(k, grid) >= 5:
                ngrid[k] = "L"
    return ngrid


def count_seen(k, grid):
    count = 0
    for dx in irange(-1, 1):
        for dy in irange(-1, 1):
            if dx or dy:
                count += int(can_see_in_dir(grid, k, dx+dy*1j))
    return count


def can_see_in_dir(grid, k, dp):
    while k in grid:
        k += dp
        if grid[k] == "#":
            return True
        if grid[k] == "L":
            return False
    return False


oldgrid = None

while oldgrid != grid:
    oldgrid, grid = grid, evolve2(grid)
    grid.draw()
    print(count_o(grid))
