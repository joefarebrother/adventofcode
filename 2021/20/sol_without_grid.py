from utils import *

enh, img = inp_groups()
enh = "".join(enh)

img = Grid(img)
bb = img.bounding_box
default = "."
img = defaultdict(lambda: default, img)
state = (img, default, bb)


def step(state):
    img, default, bb = state
    nbb = bb.expand_1()
    ndefault = enh[0] if default != "#" else enh[-1]
    nimg = defaultdict(lambda: ndefault)
    for p in nbb:
        px = ""
        for dp in Rectangle((-1, -1), (1, 1)):
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
