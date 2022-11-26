# pylint: disable=unused-wildcard-import
from utils import *


def neighbours_dim(p):
    for delta in it.product([-1, 0, 1], repeat=len(p)):
        if any(delta):
            yield tuple(x+dx for (x, dx) in zip(p, delta))

    # If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. Otherwise, the cube becomes inactive.
    # If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. Otherwise, the cube remains inactive.


def evolve(grid):
    ngrid = set()
    dim = len(next(iter(grid)))
    bs = [bounds(p[i] for p in grid) for i in range(dim)]
    for p in it.product(*(irange(l-1, h+1) for (l, h) in bs)):
        ns = len(grid & set(neighbours_dim(p)))
        if (p in grid and ns in [2, 3]) or (p not in grid and ns == 3):
            ngrid.add(p)
    return ngrid


grid = set()
for y, line in enumerate(inp_readlines()):
    for x, c in enumerate(line):
        if c == '#':
            grid.add((x, y, 0))

for i in range(6):
    grid = evolve(grid)

print(len(grid))

grid = set()
for y, line in enumerate(inp_readlines()):
    for x, c in enumerate(line):
        if c == '#':
            grid.add((x, y, 0, 0))

for i in range(6):
    grid = evolve(grid)

print(len(grid))
