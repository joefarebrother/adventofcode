from utils import *

g = Grid(0)

guard = only(p for (p,s) in g.items() if s == "^")


def go(extra=None):
    seen = set()
    p,d = (guard, Dirs.U)
    while (p,d) not in seen and p in g:
        # print(p,d)
        seen.add((p,d))
        if g[p+d] == "#" or p+d == extra:
            d *= Dirs.tR
        else:
            p += d
    if (p,d) in seen:
        print(extra,p,d)

    # return the set of visited positions (for p1 + choosing paths for p2) and whether we looped (for p2)
    return ((set(p for (p,d) in seen)), (p,d) in seen)

res = go()
print("Part 1:", len(res[0]))

# only need to consider placing the extra wall along the path 
print("Part 2:", sum(go(ex)[1] for ex in res[0] if g[ex] == "."))