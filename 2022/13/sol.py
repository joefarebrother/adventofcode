from utils import *
import json
import functools

inp = [[json.loads(p) for p in gr] for gr in inp_groups()]


def compare(p1, p2):
    if isinstance(p1, int) and isinstance(p2, int):
        return p1 - p2

    p1 = p1 if isinstance(p1, list) else [p1]
    p2 = p2 if isinstance(p2, list) else [p2]

    p1 = iter(p1)
    p2 = iter(p2)
    while True:
        try:
            p1i = next(p1)
        except StopIteration:
            try:
                next(p2)
            except StopIteration:
                return 0
            return -1
        try:
            p2i = next(p2)
        except StopIteration:
            return 1
        cmp = compare(p1i, p2i)
        if cmp != 0:
            return cmp


s = 0
for i, (p1, p2) in enumerate(inp):
    print(i, p1, p2, compare(p1, p2))
    if compare(p1, p2) <= 0:
        s += i+1


print(s)

ps = [p for gr in inp for p in gr] + [[[2]], [[6]]]
ps = sorted(ps, key=functools.cmp_to_key(compare))

indxs = []
for i, p in enumerate(ps):
    if p in [[[2]], [[6]]]:
        indxs.append(i+1)

print(math.prod(indxs))
