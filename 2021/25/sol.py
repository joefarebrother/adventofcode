from utils import *

inp = Grid(25, wrapx=True, wrapy=True, default=".")

arr = {1: ">", 1j: "v"}
changed = True


def step(g, dir):
    global changed
    ng = Grid(g, copydata=False)
    for p in g:
        if g[p] == arr[dir] and g[p+dir] == ".":
            ng[p+dir] = g[p]
            changed = True
        elif g[p] != ".":
            ng[p] = g[p]
    return ng


i = 0
g = inp
while changed:
    changed = False
    g = step(g, 1)
    g = step(g, 1j)
    i += 1
    if is_ex and i < 10:
        print(i, flush=True)
        g.draw()

print(i)
