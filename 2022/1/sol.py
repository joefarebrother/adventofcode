from utils import *

inp = inp_groups()

print(max(sum(ints(gr)) for gr in inp))

x = [sum(ints(gr)) for gr in inp]
x = sorted(x)[::-1]
print(sum(x[:3]))
