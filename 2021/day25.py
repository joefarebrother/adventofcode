from utils import *

inp = Grid(25, wrapx=True, wrapy=True)

arr = {1: ">", 1j: "v"}


def step(g, dir):
    ng = Grid(wrapx=g.wrapx, wrapy=g.wrapy, y_is_down=True, default=".")
    #printx(ng.wrapx, ng.wrapy)
    for p in g:
        if g[p] == arr[dir] and g[p+dir] not in ["v", ">"]:
            ng[p+dir] = g[p]
        elif g[p] in ["v", ">"]:
            ng[p] = g[p]
    return ng


def k(g):
    return {p: v for p, v in g.items() if v in ["v", ">"]}


i = 0
last = {}
g = inp
while k(g) != k(last):
    last = g
    g = step(g, 1)
    g = step(g, 1j)
    i += 1
    if is_ex and i < 10:
        print(i, flush=True)
        g.draw()

print(i)
