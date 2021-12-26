from utils import *

inp = inp_readlines()

minx, maxx, miny, maxy = ints_in(inp[0])
target = Rectangle((minx, miny), (maxx, maxy))


def step(p, v):
    p += v
    v -= sign(v.real)+1j
    return p, v


def hits(v):
    p = 0
    maxyp = 0
    while True:
        p, v = step(p, v)
        maxyp = max(maxyp, p.imag)
        if p in target:
            return True, maxyp
        if (p.imag < miny and v.imag < 0) or p.real > maxx:
            return False, maxyp


maxyp = 0
works = set()
for x in irange(maxx):
    for y in range(miny, 500):
        v = complex(x, y)
        h, nmaxyp = hits(v)
        if h:
            works.add(v)
            maxyp = max(maxyp, nmaxyp)

print("Part 1:", int(maxyp))
print("Part 2:", len(works))
