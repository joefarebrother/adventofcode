from collections import Counter
from utils import *

inp = readlines(14)

pol = inp[0]
origpol = pol
rules = [l.split(" -> ") for l in inp[2:]]
rules = {r: c for (r, c) in rules}


def step(p):
    res = ""
    for a, b in zip(p, p[1:]):
        ab = a+b
        if ab in rules:
            res += a+rules[ab]
        else:
            res += a
    res += b
    return res


for i in range(10):
    pol = step(pol)
    # print(pol)


c = Counter(pol)
# print(c)
print("Part 1:", max(c.values()) - min(c.values()))


@cache
def ct(char, poly, steps):
    if steps == 0:
        return poly.count(char)
    tot = 0
    for a, b in zip(poly, poly[1:]):
        ab = a+b
        if ab in rules:
            acb = a+rules[ab]+b
        else:
            acb = ab
        tot += ct(char, acb, steps-1)
        tot -= (b == char)
    tot += (b == char)
    return tot


all_chars = set(origpol) | set(rules.values())
c = {ch: ct(ch, origpol, 40) for ch in all_chars}
# print(c)
print("Part 2:", max(c.values()) - min(c.values()))
