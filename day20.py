# pylint: disable=unused-wildcard-import
from utils import *
import pickle


class D8:
    # <xa | x2 = a4 = e, xa = a-1x>
    def __init__(self, rot, flip=False):
        self.rot = rot
        self.flip = flip

    def __mul__(self, other):
        if isinstance(other, D8):
            return D8(self.rot * (1/other.rot if self.flip else other.rot), self.flip ^ other.flip)
        return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, complex):
            c = other*self.rot
            return c.conjugate() if self.flip else c
        return NotImplemented

    def inv(self):
        if self.flip:
            return self
        else:
            return D8(1/self.rot, False)

    def __eq__(self, other):
        return (self.rot, self.flip) == (other.rot, other.flip)

    def __hash__(self):
        return hash((self.rot, self.flip))

    def __repr__(self):
        return "D8" + repr((self.rot, self.flip))

    def __str__(self):
        i = [1j**i for i in range(4)].index(self.rot)
        if not i:
            return "f" if self.flip else "e"
        else:
            rs = "r" if i == 1 else f"r{i}"
            return f"{rs} * f" if self.flip else rs


r = D8(1j, False)
f = D8(1, True)
e = D8(1, False)
assert (r*r*r*r == e)
assert(f*f == e)
assert(f*r*f == r.inv())
d8 = [D8(rot, flip)
      for (rot, flip) in it.product(neighbours(0), [False, True])]
r2 = r*r
r3 = r.inv()

tiles = {}
for gr in groups("20.in"):
    gr = gr.split("\n")
    n, gr = gr[0], gr[1:]
    tiles[ints_in(n)[0]] = Grid(gr)

print(len(tiles))
sz = 10


def get_in_ori(tile, ori, pos):
    cent = 4.5+4.5j
    return tile[(pos-cent)*ori.inv()+cent]


def top_edge(tile, ori):
    r = [get_in_ori(tile, ori, x) for x in range(10)]
    assert all(x != None for x in r)
    return r


fst = next(iter(tiles))
jigsaw = Grid({0j: (fst, e)})
jig_size = int(math.sqrt(len(tiles)))
print(fst)


def compat(t1, or1, t2, or2, ed):
    # i drew a diagram to figure this out and still got it wrong like 10 times
    return top_edge(tiles[t1], or1*D8(ed.conjugate()*1j)) == top_edge(tiles[t2], or2*(D8(-ed.conjugate()*1j)))[::-1]


def fits(tile, pos, ori):
    if pos in jigsaw:
        return False
    bb = jigsaw.bounding_box + pos
    if bb.width() > jig_size or bb.height() > jig_size:
        return False
    for d in neighbours(0):
        if pos+d not in jigsaw:
            continue
        (t2, ori2) = jigsaw[pos+d]
        if not compat(tile, ori, t2, ori2, -d):
            return False
    return True


sol = None


def search(ts=set(tiles)-{fst}):
    global sol
    if not ts:
        print("Solved!")
        sol = Grid(jigsaw)
        return
    # print(ts)
    # draw_jig()
    # input()
    ps = set(p for pos in jigsaw for p in neighbours(pos))
    for t in ts:
        for p in ps:
            for ori in d8:
                if fits(t, p, ori):
                    # print(f"{t} fits in {p} at {ori} ")
                    jigsaw[p] = (t, ori)
                    search(ts-{t})
                    if sol:
                        return
                    del jigsaw[p]
                # else:
                #     print(f"{t} doesn't fit in {p} at {ori} ")


def draw_jig():
    print("jigsaw:")
    for jy in jigsaw.bounding_box.yrange():
        for y in range(sz):
            for jx in jigsaw.bounding_box.xrange():
                t = jigsaw[jx, jy]
                for x in range(sz):
                    if not t:
                        r = " "
                    else:
                        (tid, ori) = t
                        til = tiles[tid]
                        if y in [0, 9] or x in [0, 9]:
                            r = get_in_ori(til, ori, x+y*1j)
                        else:
                            tid = str(tid)
                            ori = str(ori)
                            if y == 4 and x in range(3, len(tid)+3):
                                r = tid[x-3]
                            elif y == 5 and x in range(2, len(ori)+2):
                                r = ori[x-2]
                            else:
                                r = " "
                    print(r, end="")
            print()


# 1951    2311    3079
# 2729    1427    2473
# 2971    1489    1171

try:
    jigsaw = pickle.load(open("jigsaw.pkl", "rb"))
except:
    search()
    pickle.dump(jigsaw, open("jigsaw.pkl", "wb"))
draw_jig()

cs = [jigsaw[c][0] for c in jigsaw.bounding_box.corners()]
print(cs)
print(math.prod(cs))

img = Grid()
imx, imy = 0, 0
for jy in jigsaw.bounding_box.yrange():
    for y in range(1, sz-1):
        for jx in jigsaw.bounding_box.xrange():
            t, ori = jigsaw[jx, jy]
            tile = tiles[t]
            for x in range(1, sz-1):
                if get_in_ori(tile, ori, x+y*1j) == "#":
                    img[imx, imy] = "~"
                imx += 1
        imx = 0
        imy += 1

img.draw()
monster = Grid("seamonster")
monster.draw()


def find_monsters(ori):
    found = 0
    mon = {p * ori for p in monster if monster[p] == "#"}
    # not certain this is correct in general (take the bb enclosing both bbs)
    for p in img.bounding_box + bounding_box(mon):
        if all(img[p+mp] for mp in mon):
            for mp in mon:
                img[p+mp] = "o"
            found += 1
    print(found, ori)


for ori in d8:
    find_monsters(ori)

# visualisation after determining that r was the correct orientation
Grid({p*r: v for (p, v) in img.items()}).draw()
print(list(img.values()).count("~"))
