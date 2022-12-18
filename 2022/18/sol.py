from utils import *

cubes = set()
for line in inp_readlines():
    cubes.add(tuple(ints_in(line)))


def adj(cube):
    for d in range(3):
        for dd in [-1, 1]:
            yield modify_idx(cube, d, cube[d]+dd)


tot = 0
for c in cubes:
    for ac in adj(c):
        if ac not in cubes:
            tot += 1

print("Part 1:", tot)

minp = []
maxp = []
for d in range(3):
    minp.append(min(c[d] for c in cubes)-1)
    maxp.append(max(c[d] for c in cubes)+1)

minp = tuple(minp)
maxp = tuple(maxp)

print(minp, maxp)


def adj2(c):
    for c2 in adj(c):
        if c2 not in cubes:
            for d in range(3):
                if minp[d] <= c2[d] <= maxp[d]:
                    continue
                else:
                    break
            else:
                yield c2


gr = FGraph(adj=adj2)
reachable = set()
for c, d in gr.BFS(minp):
    reachable.add(c)

print(reachable)

tot = 0
for c in cubes:
    for ac in adj(c):
        if ac in reachable and ac not in cubes:
            tot += 1

print("Part 2:", tot)
