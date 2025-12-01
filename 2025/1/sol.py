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
    tot += num 

    while tot < 0:
        tot += 100
        if not was_z:
            zer += 1 
        was_z = False

    while tot > 100:
        tot -= 100 
        zer += 1 

    if tot == 0 or tot == 100:
        zer += 1
        was_z = True 
        tot = 0
    else:
        was_z = False

    print(num, tot, zer)
    

print("Part 2:", zer)