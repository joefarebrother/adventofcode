# pylint: disable=unused-wildcard-import
from utils import *
import math

time, busses_r = readlines("13.in")
print(time)
time = int(time)
busses = ints_in(busses_r)
print(busses)

best = 1000000000000000
bestb = None

for b in busses:
    earl = math.ceil(time / b) * b
    if earl < best:
        best, bestb = earl, b
        print(b, earl)

print(bestb, (best-time), bestb*(best-time))

#busses_r = "7,13,x,x,59,x,31,19"

mods = [(int(x), (-i) % int(x))
        for (i, x) in enumerate(busses_r.split(',')) if x != 'x']
print(mods)


res = crt(mods)
print(res)

print([(res % p, p, i) for (p, i) in mods])
