from utils import *

def prune(n):
    return n % 16777216 

def step(n):
    n = prune(n*64 ^ n)
    n = prune(n//32 ^ n)
    n = prune(n*2048 ^ n)
    return n 

def step_m(n):
    for _ in range(2000):
        n = step(n)
    return n 

inp = mapl(int, inp_readlines())

print("Part 1:", sum(map(step_m,inp)))

def prices(n):
    
    for _ in range(2000):
        yield n % 10
        n = step(n)
    yield n%10
        

def changes(n):
    for pr in windows(prices(n), 5):
        lpr = pr[-1]
        changes = [b-a for a,b in windows(pr, 2)]
        yield tuple(changes), lpr

c = Counter()

for n in inp:
    seen = set()
    for ch,lpr in changes(n):
        if ch not in seen:
            seen.add(ch)
            c[tuple(ch)] += lpr 

# printx(max(c, key=c.get))
# printx(c[-2,1,-1,3])
print("Part 2:", max(c.values()))
 