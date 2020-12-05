from utils2020 import *

grid = Grid("input24")
start_grid = grid


def update(grid):
    new = Grid()
    for p, b in grid.items():
        n = count_nbhd(p, grid)
        if b == '#':
            new[p] = '#' if n == 1 else '.'
        else:
            new[p] = '#' if n == 1 or n == 2 else '.'
    return new


def count_nbhd(p, grid):
    return [grid[np] for np in neighbours(p)].count('#')


history = []

while True:
    grid.draw()
    history += [grid]
    grid = update(grid)
    if grid in history:
        break

grid.draw()
print(grid)

out = 0
k = -1
for i in range(5):
    for j in range(5):
        k += 1
        if grid[i*1j+j] == '#':
            out += 2**k

print(out)


def newgrid():
    return Grid([
        ".....",
        ".....",
        "..?..",
        ".....",
        "....."
    ])


centre = 2+2j
grid = start_grid
grid[centre] = '?'
rgrid = {0: grid, 1: newgrid(), -1: newgrid()}


def rec_update(rgrid):
    new = {}
    max_l = 0
    min_l = 0
    for level, grid in rgrid.items():
        new[level] = Grid()
        max_l = max(max_l, level)
        min_l = min(min_l, level)
        for p, b in grid.items():
            n = count_rnbhd(rgrid, level, p)
            if b == '?':
                new[level][p] = '?'
            elif b == '#':
                new[level][p] = '#' if n == 1 else '.'
            else:
                new[level][p] = '#' if n == 1 or n == 2 else '.'
    new[min_l-1] = newgrid()
    new[max_l+1] = newgrid()
    return new


def count_rnbhd(rgrid, level, p):
    count = 0
    for np in neighbours(p):
        if np in rgrid[level] and rgrid[level][np] == '#':
            count += 1
    for d in neighbours(0j):
        if p+d not in rgrid[level] and level-1 in rgrid:
            count += int(rgrid[level-1][centre+d] == '#')
        if p+d == centre and level+1 in rgrid:
            for lp, b in rgrid[level+1].items():
                if lp-d not in rgrid[level+1]:
                    count += int(b == '#')
    return count


for i in range(200):
    print("step", i)
    for level, grid in rgrid.items():
        print("depth", level)
        grid.draw()
    rgrid = rec_update(rgrid)
    count = 0
    for l, g in rgrid.items():
        for p, b in g.items():
            count += int(b == '#')
    print(i, count)

'''
print("after step", 10)
for level, grid in rgrid.items():
    print("depth", level)
    draw_grid(grid)
'''
