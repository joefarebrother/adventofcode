from utils import *

enh, img = inp_groups()
enh = "".join(enh)

img = Grid(img)
bb = [complex(p) for p in img.bounding_box.opposite_corners()]
default = "."
img = defaultdict(lambda: default, {complex(p): v for p, v in img.items()})
state = (img, default, bb)


def expand_1(bb):
    minp, maxp = bb
    return minp-1-1j, maxp+1+1j


def points(bb):
    minp, maxp = bb
    minx, miny, maxx, maxy = minp.real, minp.imag, maxp.real, maxp.imag
    for y in irange(int(miny), int(maxy)):
        for x in irange(int(minx), int(maxx)):
            yield x+y*1j


def step(state):
    img, default, bb = state
    nbb = expand_1(bb)
    ndefault = enh[0] if default != "#" else enh[-1]
    nimg = defaultdict(lambda: ndefault)
    for p in points(nbb):
        px = ""
        for dp in points((-1-1j, 1+1j)):
            px += ("1" if img[p+dp] == "#" else "0")
        nimg[p] = enh[int(px, 2)]
    return nimg, ndefault, nbb


img2, _, _ = step(step(state))
print("Part 1:", Counter(img2.values())['#'])

for i in range(50):
    print(i, len(img), flush=True)
    state = step(state)
    img = state[0]

print("Part 2:", Counter(img.values())['#'])

# sol.py: 30s
# sol_without_grid.py: 24s
# sol_pure.py: 6s
# so using IVec2 a lot is slow. How to improve?
