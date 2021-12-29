from utils import *
import dataclasses

inp = inp_readlines()

g = defaultdict(bool)
instrs = []

for line in inp:
    on = line.startswith("on")
    x0, x1, y0, y1, z0, z1 = ints_in(line)
    instrs.append((on, ints_in(line)))

for on, bnds in instrs:
    if all(abs(b) <= 50 for b in bnds):
        x0, x1, y0, y1, z0, z1 = bnds
        for x in irange(x0, x1):
            for y in irange(y0, y1):
                for z in irange(z0, z1):
                    g[x, y, z] = on

print("Part 1:", Counter(g.values())[True])


@dataclass
class Cuboid:
    x0: int
    x1: int
    y0: int
    y1: int
    z0: int
    z1: int

    def intersect(self, other):
        xint = intersect_irange((self.x0, self.x1),
                                (other.x0, other.x1))
        yint = intersect_irange((self.y0, self.y1),
                                (other.y0, other.y1))
        zint = intersect_irange((self.z0, self.z1),
                                (other.z0, other.z1))
        if xint and yint and zint:
            (x0, x1) = xint
            (y0, y1) = yint
            (z0, z1) = zint
            return Cuboid(x0, x1, y0, y1, z0, z1)
        return None

    def difference(self, other):
        res = []
        cur = dataclasses.replace(self)
        if not cur.intersect(other):
            return [cur]

        # left
        if cur.x0 < other.x0 <= cur.x1:
            ox0 = other.x0
            res.append(dataclasses.replace(cur, x1=ox0-1))
            cur.x0 = ox0
        # right
        if cur.x0 <= other.x1 < cur.x1:
            ox1 = other.x1
            res.append(dataclasses.replace(cur, x0=ox1+1))
            cur.x1 = ox1

        # front
        if cur.y0 < other.y0 <= cur.y1:
            oy0 = other.y0
            res.append(dataclasses.replace(cur, y1=oy0-1))
            cur.y0 = oy0
        # back
        if cur.y0 <= other.y1 < cur.y1:
            oy1 = other.y1
            res.append(dataclasses.replace(cur, y0=oy1+1))
            cur.y1 = oy1

        # top
        if cur.z0 < other.z0 <= cur.z1:
            oz0 = other.z0
            res.append(dataclasses.replace(cur, z1=oz0-1))
            cur.z0 = oz0
        # bottom
        if cur.z0 <= other.z1 < cur.z1:
            oz1 = other.z1
            res.append(dataclasses.replace(cur, z0=oz1+1))
            cur.z1 = oz1

        return res

    def volume(self):
        return (self.x1-self.x0+1)*(self.y1-self.y0+1)*(self.z1-self.z0+1)


cubes = []
for (on, bnds) in instrs:
    c = Cuboid(*bnds)

    if on:
        printx("Adding:", c)
        cs = [c]
        for d in cubes:
            ncs = []
            for nc in cs:
                ncs += nc.difference(d)
            cs = ncs
        printx(len(cs), "added")
        cubes += cs
    else:
        printx("Removing:", c, "from", len(cubes))
        nds = []
        for d in cubes:
            nds += d.difference(c)
        cubes = nds
        printx(len(cubes), "remain")

print("Part 2:", sum(c.volume() for c in cubes))
