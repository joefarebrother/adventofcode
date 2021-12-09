from utils import *

inp = Grid(9)
for p in inp:
    inp[p] = int(inp[p])

low = Grid(inp)
for p in low:
    low[p] = None

risk = 0
for p, v in inp.items():
    if all(dp not in inp or inp[dp] > v for dp in neighbours(p)):
        low[p] = p
        risk += v+1

print("Part 1: ", risk)


def prop_base():
    global low, inp
    changed = False
    for p in inp:
        if inp[p] != 9 and low[p] is None:
            for dp in neighbours(p):
                if dp in inp and low[dp] is not None:
                    low[p] = low[dp]
                    changed = True
    return changed


while prop_base():
    pass

ct = defaultdict(int)
for v in low.values():
    if v is not None:
        ct[v] += 1

big = sorted(ct.values(), reverse=True)[:3]
print("Part 2: ", big, math.prod(big))
