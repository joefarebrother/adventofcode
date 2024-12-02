from utils import *

inp = [ints_in(l) for l in inp_readlines()]

def safe(l):
    if l != sorted(l) and l[::-1] != sorted(l):
        printx(l, "unsort")
        return False 
    
    for a,b in windows(l, 2):
        if abs(a-b) not in [1,2,3]:
            printx(l, "diff")
            return False 
        
    printx(l, "safe")
    
    return True
        

def safe2(l):
    if safe(l):
        return True 
    
    for i in range(len(l)):
        l2 = list(l)
        l2.pop(i)
        if safe(l2):
            return True 
        
    return False

print("Part 1:", sum(mapl(safe,inp)))
print("Part 2:", sum(mapl(safe2,inp)))