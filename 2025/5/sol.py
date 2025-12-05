from utils import *

rngs, ids = inp_groups()

fresh = IntervalSet()
for r in rngs:
    a,b = ints_in(r)
    fresh |= Interval(a,b)

tot = 0
for i in ids:
    if int(i) in fresh:
        tot += 1 

print("Part 1:", tot) 
print("Part 2:", len(fresh))  