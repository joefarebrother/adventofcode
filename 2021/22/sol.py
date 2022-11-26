from utils import *
import dataclasses

inp = inp_readlines()

g = defaultdict(bool)
instrs = []

for line in inp:
    on = line.startswith("on")
    minx, maxx, miny, maxy, minz, maxz = ints_in(line)
    instrs.append((on, ints_in(line)))

for on, bnds in instrs:
    if all(abs(b) <= 50 for b in bnds):
        minx, maxx, miny, maxy, minz, maxz = bnds
        for x in irange(minx, maxx):
            for y in irange(miny, maxy):
                for z in irange(minz, maxz):
                    g[x, y, z] = on

print("Part 1:", Counter(g.values())[True])


@dataclass
class Cuboid:
    minx: int
    maxx: int
    miny: int
    maxy: int
    minz: int
    maxz: int

    def intersect(self, other):
        xint = intersect_irange((self.minx, self.maxx),
                                (other.minx, other.maxx))
        yint = intersect_irange((self.miny, self.maxy),
                                (other.miny, other.maxy))
        zint = intersect_irange((self.minz, self.maxz),
                                (other.minz, other.maxz))
        if xint and yint and zint:
            (minx, maxx) = xint
            (miny, maxy) = yint
            (minz, maxz) = zint
            return Cuboid(minx, maxx, miny, maxy, minz, maxz)
        return None

    def difference(self, other):
        res = []
        cur = dataclasses.replace(self)
        if not cur.intersect(other):
            return [cur]

        # left
        if cur.minx < other.minx <= cur.maxx:
            ominx = other.minx
            res.append(dataclasses.replace(cur, maxx=ominx-1))
            cur.minx = ominx
        # right
        if cur.minx <= other.maxx < cur.maxx:
            omaxx = other.maxx
            res.append(dataclasses.replace(cur, minx=omaxx+1))
            cur.maxx = omaxx

        # front
        if cur.miny < other.miny <= cur.maxy:
            ominy = other.miny
            res.append(dataclasses.replace(cur, maxy=ominy-1))
            cur.miny = ominy
        # front
        if cur.miny <= other.maxy < cur.maxy:
            omaxy = other.maxy
            res.append(dataclasses.replace(cur, miny=omaxy+1))
            cur.maxy = omaxy

        # top
        if cur.minz < other.minz <= cur.maxz:
            ominz = other.minz
            res.append(dataclasses.replace(cur, maxz=ominz-1))
            cur.minz = ominz
        # bottom
        if cur.minz <= other.maxz < cur.maxz:
            omaxz = other.maxz
            res.append(dataclasses.replace(cur, minz=omaxz+1))
            cur.maxz = omaxz

        return res

    def volume(self):
        return (self.maxx-self.minx+1)*(self.maxy-self.miny+1)*(self.maxz-self.minz+1)


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
