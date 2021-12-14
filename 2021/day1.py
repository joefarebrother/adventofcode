from utils import *

inp = ints(readlines(1))


def increases(xs):
    return sum(x < y for x, y in windows(xs, 2))


print("Part 1:", increases(inp))

sliding = [sum(t) for t in windows(inp, 3)]

print("Part 2:", increases(sliding))
