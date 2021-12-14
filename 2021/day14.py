from utils import *

inp = readlines(14)

pol = inp[0]
rules = [l.split(" -> ") for l in inp[2:]]
rules = {r: c for (r, c) in rules}

# original part 1 solution is in the commit history


@cache
def count(char, poly, steps):
    if steps == 0:
        return poly.count(char)
    tot = 0
    for a, b in zip(poly, poly[1:]):
        ab = a+b
        if ab in rules:
            acb = a+rules[ab]+b
        else:
            # this never happens on the given input
            acb = ab
        tot += count(char, acb, steps-1)
        tot -= (b == char)
    tot += (b == char)
    return tot


def ans(steps):
    all_chars = set(pol) | set(rules.values())
    c = [count(ch, pol, steps) for ch in all_chars]
    return max(c) - min(c)


print("Part 1:", ans(10))
print("Part 2:", ans(40))
