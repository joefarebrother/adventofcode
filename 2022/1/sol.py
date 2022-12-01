from utils import *

inp = inp_groups()
cals = [sum(ints(gr)) for gr in inp]
cals = sorted(cals, reverse=True)

print("Part 1:", cals[0])
print("Part 2:", sum(cals[:3]))
