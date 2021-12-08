from utils import *

inp = ints(readlines(1))


def increases(xs):
    return sum(x < y for x, y in zip(xs, xs[1:]))


print(increases(inp))

sliding = [sum(t) for t in zip(inp, inp[1:], inp[2:])]

print(increases(sliding))
