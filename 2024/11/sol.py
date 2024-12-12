from utils import *

stones = ints_in(inp_readall())

stones = Counter(stones)

def step(stones):
    new = Counter()
    for st,c in stones.items():
        if st == 0:
            new[1]+=c 
        elif (l:=len(strst:=str(st)))%2==0:
            new[int(strst[:l//2])] += c 
            new[int(strst[l//2:])] += c
        else:
            new[st*2024] += c
    return new

for i in range(75):
    stones = step(stones)
    if i == 25:
        print("Part 1:", stones.total())

print("Part 2:", stones.total()) 