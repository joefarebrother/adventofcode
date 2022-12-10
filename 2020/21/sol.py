# pylint: disable=unused-wildcard-import
from utils import *

food = []
als = set()
for f in inp_readlines():
    f, al = f.split(" (contains ")
    al = tuple(al[:-1].split(", "))
    ing = f.split(" ")
    food.append((frozenset(ing), al))
    als |= set(al)


poss = {}
for (ing, al) in food:
    for a in al:
        if a in poss:
            poss[a] &= ing
        else:
            poss[a] = ing

imposs = set()
for (ing, _) in food:
    for a in als:
        ing -= poss[a]
    imposs |= ing

t = 0
for (ing, _) in food:
    t += len(imposs & ing)
print("Part 1:", t)

conf = pick_uniq(poss)

c = [conf[k] for k in sorted(conf)]
print("Part 2:", ",".join(c))
