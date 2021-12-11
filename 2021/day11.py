from utils import *

grid = Grid(11)
for p in grid:
    grid[p] = int(grid[p])


def step(grid):
    flashes = set()
    for p in grid:
        grid[p] += 1
    changed = True
    while changed:
        changed = False
        for p in grid:
            if grid[p] >= 10 and p not in flashes:
                flashes.add(p)
                changed = True
                for dp in neighbours8(p):
                    if dp in grid:
                        grid[dp] += 1
    for p in flashes:
        grid[p] = 0
    return len(flashes)


c = 0
for i in range(100):
    c += step(grid)
    if i % 10 == 0 or i < 10:
        print(i)
        grid.draw(symbols={})

print("Part 1:", c)

s = 101
while step(grid) != len(grid):
    s += 1

print("Part 2:", s)
