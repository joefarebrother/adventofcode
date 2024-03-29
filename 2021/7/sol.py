from utils import *

inp = ints(inp_readlines()[0].split(","))


def tri(n):
    return n*(n+1)//2


def fuel_to1(x):
    return (sum(dist(x, i) for i in inp))


def fuel_to2(x):
    return (sum(tri(dist(x, i)) for i in inp))


print("Part 1: ", min(map(fuel_to1, inp)))
print("Part 2: ", min(map(fuel_to2, range(*bounds(inp)))))
