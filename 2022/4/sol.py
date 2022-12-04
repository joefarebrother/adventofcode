from utils import *

inp = [ints_in(x) for x in inp_readlines()]

tot1 = 0
tot2 = 0
for c1, c2, d1, d2 in inp:
    c = set(irange(c1, c2))
    d = set(irange(d1, d2))
    if c <= d or d <= c:
        tot1 += 1
    if c & d:
        tot2 += 1

print("Part 1:", tot1)
print("Part 2:", tot2)
