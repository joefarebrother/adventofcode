# pylint: disable=unused-wildcard-import
from utils import *

rules = inp_readlines()

bags = defaultdict(dict)

for line in rules:
    (root, rhs) = match(r'([a-z ]*) bags? contain ([\w, ]*)\.', line)
    if not rhs.startswith("no other"):
        for ch in rhs.split(","):
            (num, col) = match(r'(\d*) ([a-z ]*) bags?', ch, exact=False)
            bags[root][col] = num

cols = set(DGraph(bags).reverse().DFS("shiny gold"))

print(cols)
print("Part 1:", len(cols)-1)


def nest(col):
    tot = 1
    for next in bags[col]:
        tot += nest(next) * bags[col][next]
    return tot


print("Part 2:", nest("shiny gold")-1)
