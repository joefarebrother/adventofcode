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


def chinese_remainder(mods):
    """
    https://rosettacode.org/wiki/Chinese_remainder_theorem#Python
    """
    sum = 0
    prod = math.prod([p for (p, i) in mods])
    for n_i, a_i in mods:
        p = prod // n_i
        sum += a_i * mod_inv(p, n_i) * p
    return sum % prod


res = chinese_remainder(mods)
print(res)

print([(res % p, p, i) for (p, i) in mods])
