from utils import *

inp = readlines(14)

pol = inp[0]
rules = defaultdict(str, [l.split(" -> ") for l in inp[2:]])

# original part 1 solution is in the commit history


@cache
def count(poly, steps):
    if steps == 0:
        return Counter(poly)
    tot = Counter()
    for a, b in windows(poly, 2):
        acb = a+rules[a+b]+b
        tot += count(acb, steps-1)
        tot[b] -= 1  # avoid double-counting
    tot[b] += 1
    return tot


def ans(steps):
    c = count(pol, steps)
    c = list(c.values())
    return max(c) - min(c)


print("Part 1:", ans(10))
print("Part 2:", ans(40))
