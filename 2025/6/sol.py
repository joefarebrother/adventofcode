from utils import *

rows = inp_readlines()
nums = [ints_in(row) for row in rows[:-1]]
ops = rows[-1].split()

nums = zip(*nums)

tot = 0 
for op, xs in zip(ops, nums):
    if op == "+":
        tot += sum(xs)
    else:
        tot += math.prod(xs)

print("Part 1:", tot)

cols = list(zip(*rows[:-1]))[::-1]

tot = 0
ops = iter(ops[::-1])
xs = []
for c in cols + [[]]:
    n = "".join(c)
    i = ints_in(n)
    if not i:
        op = next(ops)
        if op == "+":
            tot += sum(xs)
        else:
            tot += math.prod(xs)
        xs = []
    else:
        xs.append(i[0])

print("Part 2:", tot)