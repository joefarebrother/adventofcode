from utils import *

coords, folds = groups(13)

grid = Grid()
for row in coords.splitlines():
    x, y = ints_in(row)
    grid[x, y] = 1

folds = [match(r'fold along (.)=(\d+)', f) for f in folds.splitlines()]


def do_fold(axis, line):
    global grid
    ngrid = Grid()
    for p in grid:
        x, y = pos_as(tuple, p)
        if axis == "x" and x > line:
            x = 2*line-x
        elif axis == "y" and y > line:
            y = 2*line-y
        ngrid[x, y] = 1
    # ngrid.draw()
    grid = ngrid


do_fold(*folds[0])
print(len(list(grid)))

for f in folds[1:]:
    do_fold(*f)

grid.draw(flipy=True)
