from utils import *

inp = ints(inp_readlines()[0].split(","))

amts = Counter(inp)


def step(amts):
    new = Counter()
    for i in amts:
        if i:
            new[i-1] = amts[i]
    new[6] += amts[0]
    new[8] += amts[0]
    return new


for i in irange(256):
    amts = step(amts)
    if i == 80:
        print("Part 1: ", sum(amts.values()))
    if i == 256:
        print("Part 2: ", sum(amts.values()))
