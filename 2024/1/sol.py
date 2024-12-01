from utils import *

inp = inp_readlines()

lefts, rights = zip(*[ints_in(l) for l in inp])
lefts = sorted(lefts)
rights = sorted(rights)

print("Part 1:", sum(abs(l-r) for l,r in zip(lefts,rights)))
print("Part 2:", sum(l*rights.count(l) for l in lefts))