from utils import *

rects = []
for line in inp_readlines():
    _, x, y, w, h = ints_in(line)
    rects.append(Rectangle((x, y), (x+w-1, y+h-1)))

bb = bounding_box([p for r in rects for p in r.opposite_corners()])

points = set()
for r1, r2 in it.combinations(rects, 2):
    inter = r1 & r2
    if inter:
        points |= set(inter)

print("Part 1:", len(points))

for i, r in enumerate(rects):
    if not any(r & r2 for r2 in rects if r != r2):
        print("Part 2:", i+1)
        break
