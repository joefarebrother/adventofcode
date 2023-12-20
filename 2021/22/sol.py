from utils import *

inp = inp_readlines()

g = defaultdict(bool)
instrs = []

for line in inp:
    on = line.startswith("on")
    x0, x1, y0, y1, z0, z1 = ints_in(line)
    instrs.append((on, [(x0,x1),(y0,y1),(z0,z1)]))

for on, bnds in instrs:
    if all(abs(c) <= 50 for b in bnds for c in b):
        (x0,x1),(y0,y1),(z0,z1) = bnds
        for x in irange(x0, x1):
            for y in irange(y0, y1):
                for z in irange(z0, z1):
                    g[x, y, z] = on

print("Part 1:", Counter(g.values())[True])

cubes = CuboidSet()
for (on,bds) in instrs:
    cub = Cuboid(bds)
    if on:
        cubes |= cub 
    else:
        cubes -= cub

print("Part 2:", cubes.volume())
