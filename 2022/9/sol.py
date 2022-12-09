from utils import *


def restrict(z):
    return min(1, max(z, -1))


def move(knots, d):
    knots[0] += d
    for i in range(len(knots)-1):
        diff = knots[i]-knots[i+1]
        if diff in Rectangle((-1, -1), (1, 1)):
            continue
        knots[i+1] += (restrict(diff.x), restrict(diff.y))


def do(num_knots):
    knots = [IVec2(0)]*num_knots
    vis = {knots[-1]}
    for line in inp_readlines():
        d, amt = line.split()
        amt = int(amt)
        d = Dirs[d]
        for _ in range(amt):
            move(knots, d)
            vis.add(knots[-1])
    return len(vis)


print("Part 1:", do(2))
print("Part 2:", do(10))
