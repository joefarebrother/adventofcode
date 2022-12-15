from utils import *

s_b = set()

for line in inp_readlines():
    sx, sy, bx, by = ints_in(line)
    s = IVec2(sx, sy)
    b = IVec2(bx, by)
    s_b.add((s, b, man_dist(s, b)))

bb = bounding_box([s for (s, b, d) in s_b])
maxd = max(d for (s, b, d) in s_b)
cor = bb.opposite_corners()
bb = Rectangle(cor[0]-(maxd, maxd), cor[1]+(maxd, maxd))
print(bb)

bs = set(b for (s, b, d) in s_b)

y = 10 if is_ex else 2000000

# tot = 0
# for x in bb.xrange():
#     p = IVec2(x, y)
#     if p in bs:
#         continue
#     for s, b, d in s_b:
#         if d >= man_dist(s, p):
#             printx(x)
#             tot += 1
#             break
#     else:
#         continue

row = set()
for s, b, d in s_b:
    yd = abs(s.y-y)
    if d < yd:
        continue
    d -= yd
    row |= set(irange(s.x-d, s.x+d))

row -= set(b.x for b in bs if b.y == y)
printx(row)

print("Part 1:", len(row))

maxc = 20 if is_ex else 4000000
