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

maxc = 20 if is_ex else 4000000

for y in irange(maxc):
    inter = row(y)
    if len(inter) > 1:
        assert len(inter) == 2
        (xl0, xl1), (xh0, xh1) = inter
        assert xh0 == xl1+2
        x = xl1+1
        assert 0 <= x <= maxc
        print(x, y, inter)
        print("Part 2:", 4000000*x+y)
        exit()
    if y % 100000 == 0:
        print(y, inter)

# real    0m29.956s
# user    0m29.899s
# sys     0m0.041s
