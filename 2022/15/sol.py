from utils import *

s_b = set()

for line in inp_readlines():
    sx, sy, bx, by = ints_in(line)
    s = IVec2(sx, sy)
    b = IVec2(bx, by)
    s_b.add((s, b, man_dist(s, b)))

bs = set(b for (s, b, d) in s_b)


def add_interval(intervals, interval):
    # invariant: intervals is a list of disjoint, non-adjacent intervals sorted by their lowest endpoint
    n_int = []
    x0, x1 = interval
    i = 0
    while i < len(intervals):
        y0, y1 = intervals[i]
        if y1+1 < x0:
            n_int.append((y0, y1))
        elif x1+1 < y0:
            break
        else:
            x0 = min(x0, y0)
            x1 = max(x1, y1)
        i += 1
    n_int.append((x0, x1))
    n_int += intervals[i:]
    return n_int


def row(y):
    intervals = []
    for s, _, d in s_b:
        sx, sy = s.x, s.y
        yd = abs(sy-y)
        if d < yd:
            continue
        d -= yd
        intervals = add_interval(intervals, (sx-d, sx+d))
    return intervals


p1y = 10 if is_ex else 2000000
inter = row(p1y)
x0, x1 = only(inter)

print("Part 1:", x1-x0+1 - sum(1 for b in bs if b.y == p1y))

# rotated coord system: ((x+y),(x-y))
# .x#..    (2,0),(1,1),(2,1),(3,1),(2,2)    ..#.#..
# .###. =>    (1,0)(3,2) v   (1,1)(5,1)  => .x.#.y.
# ..#y.    (2,2),(2,0),(3,1),(4,2),(4,0)    ..#.#..
#
# the new space has some points that map back to .5 offsets; e.g.
# the point (3,0) maps back to (1.5,1.5)
# we can just ignore these points; our rectangles including the desired points still function,
# and the single point we're searching for will end up in a rect of size at most 2


def rotate(p):
    x, y = p.x, p.y
    rx, ry = x+y, x-y
    rp = IVec2(rx, ry)
    assert rotate_back(rp) == p
    return rp


def rotate_back(rp):
    rx, ry = rp.x, rp.y
    x, y = (rx+ry)/2, (rx-ry)/2
    if x == int(x) and y == int(y):
        return IVec2(x, y)
    return None


def rect_for_scanner(s, d):
    res_min = s-(d, 0)
    res_max = s+(d, 0)
    res_min_r = rotate(res_min)
    res_max_r = rotate(res_max)
    res = Rectangle(res_min_r, res_max_r)
    assert rotate(s-(0, d)) in res.corners()
    assert rotate(s+(0, d)) in res.corners()

    return res


maxc = 20 if is_ex else 4000000

rects = [Rectangle((-maxc*2, -maxc*2), (maxc*2, maxc*2))]
if is_ex:
    for p in Rectangle((0, 0), (maxc, maxc)):
        assert rotate(p) in rects[0]


def rect_list_diff(rs, dr):
    res = []
    for r in rs:
        for nr in r.difference(dr):
            res.append(nr)
    return res


for s, b, d in s_b:
    rects = rect_list_diff(rects, rect_for_scanner(s, d))


for r in rects:
    if len(r) <= 2:
        for rp in r:
            p = rotate_back(rp)
            if p and p in Rectangle((0, 0), (maxc, maxc)):
                print(p)
                print("Part 2:", 4000000*p.x+p.y)
                exit()

print("Part 2: ???")
