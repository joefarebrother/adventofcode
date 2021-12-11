from utils import *
from random import randint

grid = Grid(11)
for p in grid:
    grid[p] = randint(0, 9)


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


def state(grid):
    return tuple(grid[x, y] for x in range(10) for y in range(10))


seen = {}

s = 1
while step(grid) != len(grid):
    st = state(grid)
    if st in seen:
        last = seen[st]
        period = s - last
        #grid.draw(symbols={0: " "})
        print("Cycle", last, s, period)
        if period % 7 != 0:
            print("Not divisible by 7")
            grid.draw(symbols=None)
        exit()
    else:
        seen[st] = s

    s += 1
    # if s % 100 == 0:
    #     print(s)
    #     grid.draw(symbols={0: " "})

print("Terminates", s)
