from re import L
from utils import *

inp = [ints_in(l) for l in readlines(5)]

straight_lines = []
diags = []

for ((x1, y1, x2, y2), l) in zip(inp, inp):
    r = Rectangle((x1, y1), (x2, y2))
    if r.height() == 1 or r.width() == 1:
        straight_lines.append(r)
    else:
        diags.append(l)

grid = Grid()

print(len(straight_lines), len(diags))


def inc(x, y=None):
    if y == None:
        pos = x
    else:
        pos = x, y
    grid[pos] = grid[pos] + 1 if grid[pos] else 1


def count():
    c = 0
    for p in grid:
        if grid[p] > 1:
            c += 1
    return c


for r in straight_lines:
    for p in r:
        inc(p)

print("Part 1: ", count())

for (x1, y1, x2, y2) in diags:
    xstep = sign(x2-x1)
    ystep = sign(y2-y1)
    y = y1
    for x in irange(x1, x2, xstep):
        inc(x, y)
        y += ystep

print("Part 2: ", count())
