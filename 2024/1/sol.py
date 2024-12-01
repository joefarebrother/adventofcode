from utils import *

inp = inp_readlines()

rlefts, rights = zip(*[ints_in(l) for l in inp])
lefts = sorted(rlefts)
rights = sorted(rights)

print(sum(abs(l-r) for l,r in zip(lefts,rights)))

t = 0 
for l in rlefts:
    t += l * rights.count(l)
print(t)