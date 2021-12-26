from utils import *

enh, img = inp_groups()
enh = "".join(enh)

img = Grid(img)


def step(img):
    nimg = Grid(default=enh[0] if img.default != "#" else enh[-1])
    for p in img.bounding_box.expand_1():
        px = ""
        for dp in Rectangle(-1-1j, 1+1j):
            px += ("1" if img[p+dp] == "#" else "0")
        nimg[p] = enh[int(px, 2)]
    return nimg


def run(n):
    im = img
    for _ in range(n):
        im = step(im)
    return im.count("#")


for i in range(50):
    print(i, len(img), flush=True)
    img = step(img)

print("Part 1:", run(2))
print("Part 2:", run(50))
