# pylint: disable=unused-wildcard-import
from utils import *
from itertools import *


grid = readlines("input3")
trees = 0


def check_tree(pos: complex):
    return grid[int(pos.imag)][int(pos.real) % (len(grid[0]))] == '#'


def trees_for_slope(slope):
    trees = 0

    pos = 0j
    while pos.imag < len(grid):
        if check_tree(pos):
            trees += 1

        pos += slope

    return trees


slopes = [1+1j, 3+1j, 5+1j, 7+1j, 1+2j]
treecounts = mapl(trees_for_slope, slopes)

print(treecounts)
print(math.prod(treecounts))
