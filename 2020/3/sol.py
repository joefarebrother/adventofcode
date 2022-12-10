# pylint: disable=unused-wildcard-import
from utils import *
from itertools import *


grid = Grid("input3", wrapx=True)
trees = 0

grid.draw()
print(grid.width(), grid.height())


def check_tree(pos: complex):
    return grid[pos] == '#'


def trees_for_slope(slope):
    trees = 0

    pos = 0j
    while pos in grid:
        if check_tree(pos):
            trees += 1
        #     grid[pos] = 'X'
        # else:
        #     grid[pos] = 'O'

        pos += slope

    return trees


slopes = [1+1j, 3+1j, 5+1j, 7+1j, 1+2j]
treecounts = mapl(trees_for_slope, slopes)

print(treecounts)
print("Part 1:", treecounts[0])
print("Part 2:", math.prod(treecounts))
