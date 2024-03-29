from utils import *

enh, img = inp_groups()
enh = "".join(enh)

img = Grid(img)


def step(img):
    nimg = Grid(default=enh[0] if img.default != "#" else enh[-1])
    for p in img.bounding_box.expand_1():
        px = ""
        for p1 in Rectangle(p-(1, 1), p+(1, 1)):
            px += ("1" if img[p1] == "#" else "0")
        nimg[p] = enh[int(px, 2)]
    return nimg


def run(n):
    im = img
    for i in range(n):
        im = step(im)
        print(i, len(im), flush=True)
    return im.count("#")


print("Part 1:", run(2))
print("Part 2:", run(50))
