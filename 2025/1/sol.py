from utils import *

nums = []

for line in inp_readlines():
    nums.append(int(line.replace("L","-").replace("R","+")))

zer = 0 
tot = 50 
for num in nums:
    tot += num 
    tot %= 100
    if tot == 0:
        zer += 1 

print("Part 1:", zer)

zer = 0 
tot = 50 
was_z = False
for num in nums:
    zer += abs(num)//100 
    
    for _ in range(abs(num)%100):
        tot += sign(num)
        tot %= 100
        if tot == 0:
            zer += 1
    

print("Part 2:", zer)