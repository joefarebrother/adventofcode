from utils import *

inp = inp_readlines()

g = defaultdict(bool)
instrs = []

for line in inp:
    on = line.startswith("on")
    x0, x1, y0, y1, z0, z1 = ints_in(line)
    instrs.append((on, [(x0, y0, z0), (x1, y1, z1)]))

for on, bnds in instrs:
    if all(abs(c) <= 50 for b in bnds for c in b):
        (x0, y0, z0), (x1, y1, z1) = bnds
        for x in irange(x0, x1):
            for y in irange(y0, y1):
                for z in irange(z0, z1):
                    g[x, y, z] = on

print("Part 1:", Counter(g.values())[True])


@dataclass
class Cuboid:
    los: tuple[int]
    his: tuple[int]

    def intersect(self, other):
        lores = []
        hires = []
        for s0, s1, o0, o1 in zip(self.los, self.his, other.los, other.his, strict=True):
            rint = intersect_irange((s0, s1), (o0, o1))
            if rint:
                r0, r1 = rint
                lores.append(r0)
                hires.append(r1)
            else:
                return None
        return Cuboid(tuple(lores), tuple(hires))

    def difference(self, other):
        res = []
        if not self.intersect(other):
            return [self]

        locur = list(self.los)
        hicur = list(self.his)

        for d, (c0, c1, o0, o1) in enumerate(zip(locur, hicur, other.los, other.his, strict=True)):
            #       oooooooooooooo              oooooooooooooo
            #       o            o              o            o
            #  ccccccccccc       o         rrrrrcccccc       o
            #  c    o    c       o         r   rc    c       o
            #  c    o    c       o         r   rc    c       o
            #  c    ooooocoooooooo    =>   r   rcoooocoooooooo
            #  c         c                 r   rc    c
            #  c         c                 r   rc    c
            #  c         c                 r   rc    c
            #  c         c                 r   rc    c
            #  c         c                 r   rc    c
            #  ccccccccccc                 rrrrrcccccc
            #

            # left
            if c0 < o0 <= c1:
                res.append((tuple(locur), modify_idx(tuple(hicur), d, o0-1)))
                locur[d] = o0
            # right
            if c0 <= o1 < c1:
                res.append((modify_idx(tuple(locur), d, o1+1), tuple(hicur)))
                hicur[d] = o1

        res2 = []
        for (rlo, rhi) in res:
            res2.append(Cuboid(tuple(rlo), tuple(rhi)))

        return res2

    def volume(self):
        return math.prod(c1-c0+1 for c0, c1 in zip(self.los, self.his, strict=True))


cubes = []
for (on, bnds) in instrs:
    c = Cuboid(*bnds)

    if on:
        # printx("Adding:", c)
        cs = [c]
        for d in cubes:
            ncs = []
            for nc in cs:
                ncs += nc.difference(d)
            cs = ncs
        # printx(len(cs), "added")
        cubes += cs
    else:
        # printx("Removing:", c, "from", len(cubes))
        nds = []
        for d in cubes:
            nds += d.difference(c)
        cubes = nds
        # printx(len(cubes), "remain")

print("Part 2:", sum(c.volume() for c in cubes))
