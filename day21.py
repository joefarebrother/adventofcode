# pylint: disable=unused-wildcard-import
from utils import *

food = []
als = set()
for f in readlines("21.in"):
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

print(imposs)
t = 0
for (ing, _) in food:
    t += len(imposs & ing)
print(t)

# copy-paste day 16
conf = {}
while True:
    for al in poss:
        if len(poss[al]) == 1:
            ing = list(poss[al])[0]
            conf[ing] = [al]
            break
    else:
        break
    for al in poss:
        if ing in poss[al]:
            poss[al] -= {ing}

print(poss, conf)
c = sorted(conf, key=lambda k: conf[k])
print(",".join(c))
