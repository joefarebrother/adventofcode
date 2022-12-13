from utils import *
import json
import functools

inp = [[json.loads(p) for p in gr] for gr in inp_groups()]


def compare(p1, p2):
    if isinstance(p1, int) and isinstance(p2, int):
        return p1 - p2

    p1 = p1 if isinstance(p1, list) else [p1]
    p2 = p2 if isinstance(p2, list) else [p2]

    for p1i, p2i in zip(p1, p2):
        cmp = compare(p1i, p2i)
        if cmp != 0:
            return cmp

    return len(p1) - len(p2)


s = 0
for i, (p1, p2) in enumerate(inp):
    if compare(p1, p2) <= 0:
        s += i+1


print("Part 1:", s)

div = [[[2]], [[6]]]
ps = [p for gr in inp for p in gr] + div
ps = sorted(ps, key=functools.cmp_to_key(compare))

indxs = []
for i, p in enumerate(ps):
    if p in div:
        indxs.append(i+1)

print("Part 2:", math.prod(indxs))
