from utils import *

ranges = mapl(ints_in, inp_readall().replace("\n", "").split(","))


print(ranges)
print("max range:", max(b-a for a,b in ranges))

def invalid(n):
    n = str(n)
    return n[:len(n)//2] == n[len(n)//2:]

tot = 0
for a,b in ranges:
    for x in irange(a,b):
        if invalid(x):
            tot += x 

print("Part 1:", tot)

def invalid2(n):
    n = str(n)
    for i in range(1,len(n)-1):
        if len(n)%i != 0:
            continue
        spl = chunks(n,i)
        if len(set(spl)) == 1:
            return True
    return False

tot = 0
for a,b in ranges:
    for x in irange(a,b):
        if invalid2(x):
            tot += x 
print("Part 2:", tot)