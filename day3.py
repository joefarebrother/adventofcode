from utils import *

inp = readlines(3)


def most_common(pos, xs):  # 1 on a tie
    bits = [x[pos] for x in xs]
    if bits.count("0") > bits.count("1"):
        return "0"
    else:
        return "1"


def least_common(pos, xs):  # 0 on a tie
    return str(1-int(most_common(pos, xs)))


bitlen = len(inp[0])

gam = ""
eps = ""

for i in range(bitlen):
    gam += most_common(i, inp)
    eps += least_common(i, inp)

gam, eps = int(gam, 2), int(eps, 2)
print("Part 1: ", gam, eps, gam*eps)


def filter_pos(pos, xs, rating):
    bit = rating(pos, xs)
    return [x for x in xs if x[pos] == bit]


def filter(xs, rating):
    for i in range(bitlen):
        xs = filter_pos(i, xs, rating)
        if len(xs) == 1:
            return xs[0]


ox = filter(inp, most_common)
co2 = filter(inp, least_common)

ox, co2 = int(ox, 2), int(co2, 2)

print("Part 2: ", ox, co2, ox*co2)
