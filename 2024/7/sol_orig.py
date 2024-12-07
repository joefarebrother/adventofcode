from utils import *

eqs = []
for line in inp_readlines():
    nums = ints_in(line)
    eqs.append((nums[0], nums[1:]))

def possible(eq, part):
    tar, inp = eq
    print(eq, len(inp)-1)
    for way in itertools.product("+*|"[:part+1], repeat=len(inp)-1):
        res = inp[0]
        for op,nxt in zip(way,inp[1:],strict=True):
            #print(way, inp, nxt)
            res = res+nxt if op=="+" else res*nxt if op == "*" else int(str(res)+str(nxt))
            if res > tar: break 
        else:
            if res == tar:
                return True 
    return False 

print("Part 1:", sum(eq[0] for eq in eqs if possible(eq))) 
print("Part 2:", sum(eq[0] for eq in eqs if possible(eq))) 

