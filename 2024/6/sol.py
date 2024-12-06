from utils import *

g = Grid(0)

gaurd = only(p for (p,s) in g.items() if s in "^v<>")

p,origd = (gaurd, Dirs[g[gaurd]])


def go(extra=None):
    seen = set()
    p,d = (gaurd, origd)
    if extra:
        orig = g[extra]
        g[extra] = "#"
        assert orig==".", (extra, orig)
    while (p,d) not in seen and p in g:
        # print(p,d)
        seen.add((p,d))
        if g[p+d] == "#":
            d *= Dirs.tR
        else:
            p += d
    if extra:
        g[extra]= orig
    if (p,d) in seen:
        print(extra,p,d)
    return ((set([p for (p,d) in seen])), (p,d) in seen)

res = go()
print("Part 1:", len(res[0]))

print("Part 2:", sum(go(ex)[1] for ex in res[0] if g[ex] == "."))