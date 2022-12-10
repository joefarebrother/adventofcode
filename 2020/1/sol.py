# pylint: disable=unused-wildcard-import
from itertools import *
from utils import *
data = ints(inp_readlines())

# not my original solution; that's in the commit history


def f(n):
    for xs in combinations(data, n):
        if sum(xs) == 2020:
            print(f"Part {n-1}:", xs, math.prod(xs))


f(2)
f(3)
