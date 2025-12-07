from utils import *

rows = inp_readlines()
nums = [ints_in(row) for row in rows[:-1]]
ops = rows[-1].split()

nums = zip(*nums)

def do_op(op, xs):
    if op == "+":
        return sum(xs)
    else:
        return math.prod(xs)

print("Part 1:", sum(do_op(op,xs) for op,xs in zip(ops,nums)))

cols = list(zip(*rows[:-1]))[::-1]

tot = 0
ops = iter(ops[::-1])
xs = []
for c in cols + [[]]:
    ns = ints_in("".join(c))
    if not ns:
        op = next(ops)
        tot += do_op(op,xs)
        xs = []
    else:
        xs.append(ns[0])

print("Part 2:", tot)