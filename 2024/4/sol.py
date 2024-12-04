from utils import *

g = Grid(0, default="")

def xmas(p):
    printx(p, ["".join(g[p+am*d] for am in range(4)) for d in neighbours8(0)])
    return  ["".join(g[p+am*d] for am in range(4)) for d in neighbours8(0)].count("XMAS")

def mas(p):
    if g[p] != "A":
        return False
    return set(g[p+(1,1)]+g[p+(-1,-1)]) == set("MS") and set(g[p+(1,-1)]+g[p+(-1,1)]) == set("MS")

print("Part 1:", sum(xmas(p) for p in g))
print("Part 2:", sum(mas(p) for p in g))