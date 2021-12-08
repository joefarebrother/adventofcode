from utils import *

inp = ints(readlines(6)[0].split(","))

amts = defaultdict(int)
for i in inp:
    amts[i] += 1


def step(amts):
    new = defaultdict(int)
    for i in amts:
        if i:
            new[i-1] = amts[i]
    new[6] += amts[0]
    new[8] += amts[0]
    return new


for i in range(256):
    amts = step(amts)
    if i == 79:
        print("Part 1: ", sum(amts.values()))
    if i == 255:
        print("Part 2: ", sum(amts.values()))
