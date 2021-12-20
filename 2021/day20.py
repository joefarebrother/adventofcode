from utils import *

enh, img = groups(20)
enh = enh.replace("\n", "")

img = Grid(img.splitlines())


def step(img):
    nimg = Grid(default=enh[0] if img.default != "#" else enh[-1])
    for p in img.bounding_box.expand_1():
        px = ""
        for y in irange(-1, 1):
            for x in irange(-1, 1):
                px += ("1" if img[p+x+y*1j] == "#" else "0")
        nimg[p] = enh[int(px, 2)]
    return nimg


img2 = step(step(img))
c = Counter(img2.values())
print("Part 1:", c['#'])

for _ in range(50):
    img = step(img)

c = Counter(img.values())
print("Part 2", c['#'])
