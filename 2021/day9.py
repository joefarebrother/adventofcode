from utils import *

inp = Grid(9, default=9)
for p in inp:
    inp[p] = int(inp[p])

low = set()

risk = 0
for p, v in inp.items():
    if all(dp not in inp or inp[dp] > v for dp in neighbours(p)):
        low.add(p)
        risk += v+1

print("Part 1: ", risk)


def adj(p):
    return [dp for dp in neighbours(p) if inp[dp] != 9]


ct = []
for l in low:
    ct.append(sum(1 for _ in FGraph(adj).BFS_gen(l)))

big = sorted(ct, reverse=True)[:3]
print("Part 2: ", big, math.prod(big))
