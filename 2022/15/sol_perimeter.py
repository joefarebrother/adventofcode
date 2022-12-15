from utils import *

s_b = set()

for line in inp_readlines():
    sx, sy, bx, by = ints_in(line)
    s = IVec2(sx, sy)
    b = IVec2(bx, by)
    s_b.add((s, b, man_dist(s, b)))

# part 1 omitted

maxc = 20 if is_ex else 4000000


def perimeter(s, d):
    p = s + (d+1, 0)
    px, py = p
    for dx, dy in [(-1, 1), (-1, -1), (1, -1), (1, 1)]:
        for _ in range(d+1):
            if 0 <= px <= maxc and 0 <= py <= maxc:
                yield px, py
            px += dx
            py += dy


def man_dist_(p, s):
    px, py = p
    sx, sy = s
    return abs(px-sx) + abs(py-sy)


for s, _, d in s_b:
    print(s, d)
    for p in perimeter(s, d):
        for s2, _, d2 in s_b:
            if man_dist_(p, s2) <= d2:
                break
        else:
            print(p)
            print("Part 2: ", 4000000*p[0]+p[1])
            exit()

# real    2m9.995s
# user    2m9.692s
# sys     0m0.182s
# with the overhead of ivec2, it runs out of memory; and if the caching behaviour is removed then it takes ages.

# whereas sol.py is as follows when part 1 code is commented out.
# real    0m0.091s
# user    0m0.085s
# sys     0m0.006s
