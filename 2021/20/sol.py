from utils import *

enh, img = inp_groups()
enh = "".join(enh)

img = Grid(img)


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
print("Part 1:", img2.count('#'))

for _ in range(50):
    img = step(img)

print("Part 2:", img.count('#'))
