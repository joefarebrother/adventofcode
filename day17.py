# pylint: disable=unused-wildcard-import
from utils import *

grid = defaultdict(lambda: ".")
for y, line in enumerate(readlines("17.in")):
    for x, c in enumerate(line):
        grid[x, y, 0] = c


def neighbours3d(p):
    x, y, z = p
    for dx, dy, dz in itertools.product(irange(-1, 1), repeat=3):
        if dx or dy or dz:
            yield x+dx, y+dy, z+dz

    # If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. Otherwise, the cube becomes inactive.
    # If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. Otherwise, the cube remains inactive.


def neighbours4d(p):
    x, y, z, w = p
    for dx, dy, dz, dw in itertools.product(irange(-1, 1), repeat=4):
        if dx or dy or dz or dw:
            yield x+dx, y+dy, z+dz, w+dw


def evolve3d(grid):
    ngrid = defaultdict(lambda: ".")
    keys = [k for k in grid.keys() if grid[k] == '#']
    minx, maxx = min(x for x, y, z in keys), max(x for x, y, z in keys)
    miny, maxy = min(y for x, y, z in keys), max(y for x, y, z in keys)
    minz, maxz = min(z for x, y, z in keys), max(z for x, y, z in keys)
    for xyz in itertools.product(irange(minx-1, maxx+1), irange(miny-1, maxy+1), irange(minz-1, maxz+1)):
        ns = [grid[k] for k in neighbours3d((xyz))].count("#")
        if (grid[xyz] == '#' and ns in [2, 3]) or (grid[xyz] != '#') and ns == 3:
            ngrid[xyz] = '#'
    return ngrid


def evolve4d(grid):
    ngrid = defaultdict(lambda: ".")
    keys = [k for k in grid.keys() if grid[k] == '#']
    minx, maxx = min(x for x, y, z, w in keys), max(x for x, y, z, w in keys)
    miny, maxy = min(y for x, y, z, w in keys), max(y for x, y, z, w in keys)
    minz, maxz = min(z for x, y, z, w in keys), max(z for x, y, z, w in keys)
    minw, maxw = min(w for x, y, z, w in keys), max(w for x, y, z, w in keys)
    for xyzw in itertools.product(irange(minx-1, maxx+1), irange(miny-1, maxy+1), irange(minz-1, maxz+1), irange(minw-1, maxw+1)):
        ns = [grid[k] for k in neighbours4d((xyzw))].count("#")
        if (grid[xyzw] == '#' and ns in [2, 3]) or (grid[xyzw] != '#') and ns == 3:
            ngrid[xyzw] = '#'
    return ngrid


for i in range(6):
    grid = evolve3d(grid)

grid = defaultdict(lambda: ".")
for y, line in enumerate(readlines("17.in")):
    for x, c in enumerate(line):
        grid[x, y, 0, 0] = c

for i in range(6):
    grid = evolve4d(grid)

print(list(grid.values()).count('#'))
