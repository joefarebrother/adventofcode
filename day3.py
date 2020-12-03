# pylint: disable=unused-wildcard-import
from utils import *
from itertools import *


grid = list(open("input3"))
grid = mapl(list, grid)
trees = 0


def trees_for_slope(xinc, yinc):
    trees = 0

    xpos, ypos = 0, 0
    while ypos+yinc < len(grid):
        #print(xinc, yinc, xpos, ypos, grid[ypos][xpos])
        ypos += yinc
        xpos += xinc

        xpos %= (len(grid[0])-1)
        if grid[ypos][xpos] == '#':
            trees += 1

    return trees


slopes = [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]
treecounts = []
for (x, y) in slopes:
    treecounts.append(trees_for_slope(y, x))

print(treecounts)
print(math.prod(treecounts))
