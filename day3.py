# pylint: disable=unused-wildcard-import
from utils import *
from itertools import *


grid = readlines("input3")
trees = 0


def trees_for_slope(xinc, yinc):
    trees = 0

    xpos, ypos = 0, 0
    while ypos < len(grid):
        if grid[ypos][xpos] == '#':
            trees += 1

        ypos += yinc
        xpos += xinc
        xpos %= len(grid[0])

    return trees


slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
treecounts = mapl(lambda xy: trees_for_slope(xy[0], xy[1]), slopes)

print(treecounts)
print(math.prod(treecounts))
