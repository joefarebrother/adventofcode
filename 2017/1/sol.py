from utils import *

inp = inp_readall().strip()


s = 0
for d, nd in zip(inp, inp[1:]+inp[0]):
    if d == nd:
        s += int(d)

print("Part 1:", s)

s = 0
for i, d in enumerate(inp):
    if d == inp[(i+len(inp)//2) % len(inp)]:
        s += int(d)

print("Part 2:", s)
