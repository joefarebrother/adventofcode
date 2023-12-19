from utils import *

s_b = set()

for line in inp_readlines():
    sx, sy, bx, by = ints_in(line)
    s = IVec2(sx, sy)
    b = IVec2(bx, by)
    s_b.add((s, b, man_dist(s, b)))

bs = set(b for (s, b, d) in s_b)


def row(y):
    intervals = IntervalSet()
    for s, _, d in s_b:
        sx, sy = s.x, s.y
        yd = abs(sy-y)
        if d < yd:
            continue
        d -= yd
        intervals |= (sx-d, sx+d)
    return intervals


p1y = 10 if is_ex else 2000000
inter = row(p1y) 
ointer = only(inter.intervals)

print("Part 1:", ointer.len - sum(1 for b in bs if b.y == p1y))

maxc = 20 if is_ex else 4000000

for y in irange(maxc):
    inter = row(y)
    inter = inter.intervals
    if len(inter) > 1:
        assert len(inter) == 2
        (xl0, xl1), (xh0, xh1) = [i.tupi for i in inter]
        assert xh0 == xl1+2, (xl0,xl1,xh0,xh1)
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
