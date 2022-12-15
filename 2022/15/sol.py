from utils import *

s_b = set()

for line in inp_readlines():
    sx, sy, bx, by = ints_in(line)
    s = IVec2(sx, sy)
    b = IVec2(bx, by)
    s_b.add((s, b, man_dist(s, b)))

bs = set(b for (s, b, d) in s_b)

y = 10 if is_ex else 2000000

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

# rotated coord system: ((x+y),(x-y))
# .x#..    (2,0),(1,1),(2,1),(3,1),(2,2)    ..#.#..
# .###. =>    (1,0)(3,2) v   (1,1)(5,1)  => .x.#.y.
# ..#y.    (2,2),(2,0),(3,1),(4,2),(4,0)    ..#.#..
#
# the point (3,0) maps back to (1.5,1.5)
# so consider that/2 for even points and use 2 grids


def rotate(p):
    x, y = p.x, p.y
    rx, ry = x+y, x-y
    rp, i = IVec2(rx//2, ry//2), (rx) % 2
    assert rotate_back(rp, i) == p
    return rp, i


def rotate_back(rp, i):
    rx, ry = rp.x, rp.y
    rx *= 2
    ry *= 2
    rx += i
    ry += i
    x, y = (rx+ry)//2, (rx-ry)//2
    p = IVec2(x, y)
    # assert rotate(p) == (rp, i)
    return p


def rects(s, d):
    outer_min = s-(d, 0)
    outer_max = s+(d, 0)
    inner_min = s-(d-1, 0)
    inner_max = s+(d-1, 0)
    outer_min_r, oi1 = rotate(outer_min)
    outer_max_r, oi2 = rotate(outer_max)
    assert oi1 == oi2
    inner_min_r, ii1 = rotate(inner_min)
    inner_max_r, ii2 = rotate(inner_max)
    assert ii1 == ii2
    assert oi1 == 1-ii1
    outer = Rectangle(outer_min_r, outer_max_r)
    inner = Rectangle(inner_min_r, inner_max_r)
    assert rotate(s-(0, d))[0] in outer.corners()
    assert rotate(s+(0, d))[0] in outer.corners()
    assert rotate(s-(0, d-1))[0] in inner.corners()
    assert rotate(s+(0, d-1))[0] in inner.corners()

    if oi1 == 0:
        return outer, inner
    else:
        return inner, outer


maxc = 20 if is_ex else 4000000

rs1, rs2 = ([Rectangle((-maxc, -maxc), (maxc, maxc))] for _ in range(2))
if is_ex:
    for p in Rectangle((0, 0), (maxc, maxc)):
        rp, i = rotate(p)
        assert rp in [rs1, rs2][i][0], (p, rp, i)


def rect_list_diff(rs, dr):
    res = []
    for r in rs:
        for nr in r.difference(dr):
            res.append(nr)
    return res


for s, b, d in s_b:
    r1, r2 = rects(s, d)
    rs1 = rect_list_diff(rs1, r1)
    rs2 = rect_list_diff(rs2, r2)
    if is_ex:
        for p in Rectangle((0, 0), (maxc, maxc)):
            if man_dist(p, s) <= d:
                rp, i = rotate(p)
                assert rp in [r1, r2][i]
                assert all((rp not in r) for r in (rs1, rs2)[i]), (p, s, d)


def done(p):
    print(p)
    print("Part 2:", 4000000*p.x+p.y)
    exit()


for r in rs1:
    if len(r) == 1:
        p = rotate_back(list(r)[0], 0)
        if p in Rectangle((0, 0), (maxc, maxc)):
            done(p)

for r in rs2:
    if len(r) == 1:
        p = rotate_back(list(r)[0], 1)
        if p in Rectangle((0, 0), (maxc, maxc)):
            done(p)

print("Part 2: ???")
