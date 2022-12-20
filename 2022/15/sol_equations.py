from utils import *

s_b = set()

for line in inp_readlines():
    sx, sy, bx, by = ints_in(line)
    s = IVec2(sx, sy)
    b = IVec2(bx, by)
    s_b.add((s, b, man_dist(s, b)))

bs = set(b for (s, b, d) in s_b)

# part 1 omitted

pos_y_intersects = set()
neg_y_intersects = set()


def pos_line(p):
    """Adds to pos_y_intercepts the y-intercept of the line with slope 1 that passes through p"""
    # y = x + c
    # c = (p.y-p.x)
    pos_y_intersects.add(p.y - p.x)


def neg_line(p):
    """Adds to neg_y_intercepts the y-intercept of the line with slope -1 that passes through p"""
    # y = -x + c
    # c = (p.x+p.y)
    neg_y_intersects.add(p.x + p.y)


for i, (s, _, d) in enumerate(s_b):
    pos_line(s-(d, 0))
    neg_line(s-(d, 0))
    pos_line(s+(d, 0))
    neg_line(s+(d, 0))


# pos_y_intersects now contains the y-intersects of each line that passes through the perimeter of a sensor.
# the target point must be on a line whose y-intersect is exactly between two of those.
# same for neg.

pos_y2 = set()
neg_y2 = set()

pos_y_intersects = {y+1 for y in pos_y_intersects if y+2 in pos_y_intersects}
neg_y_intersects = {y+1 for y in neg_y_intersects if y+2 in neg_y_intersects}


maxc = 20 if is_ex else 4000000
bb = Rectangle((0, 0), (maxc, maxc))

for c, d in it.product(pos_y_intersects, neg_y_intersects):
    # y = x + c
    # y = -x + d
    # 2y = c+d
    # 2x = d-c
    y2 = c+d
    x2 = d-c
    if x2 % 2 == 1 or y2 % 2 == 1:
        continue
    p = IVec2(x2//2, y2//2)
    if p in bb:
        for s, _, d in s_b:
            if man_dist(p, s) <= d:
                break
        else:
            print("Part 2:", p.x*4000000+p.y)
            exit()

# just as fast as sol.py (~0.12s)
