# pylint: disable=unused-wildcard-import
from utils import *

rules = readlines("input7")

bags = defaultdict(dict)

for line in rules:
    (root, rhs) = match(r'([a-z ]*) bags? contain (.*)', line)
    if not rhs.startswith("no other"):
        for ch in rhs.split(","):
            (num, col) = match(r'(\d*) ([a-z ]*) bags?', ch, exact=False)
            bags[root][col] = num

bagsgr = DGraph(bags)


def f(bag):
    return bagsgr.DFS(bag, "shiny gold")[0]


cols = set()

for b in bags:
    # print(b)
    if f(b):
        cols.add(b)

cols.remove("shiny gold")

print(cols)
print(len(cols))


def nest(col):
    tot = 1
    for next in bags[col]:
        tot += nest(next) * bags[col][next]
    return tot


print(nest("shiny gold")-1)
