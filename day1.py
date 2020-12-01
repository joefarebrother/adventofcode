import math
from itertools import product
from utils import *
data = ints(list(open("input1")))

# not my original solution; that's in the commit history


def f(n):
    for xs in product(data, repeat=n):
        if sum(xs) == 2020:
            print(math.prod(xs), xs)


f(2)
f(3)
