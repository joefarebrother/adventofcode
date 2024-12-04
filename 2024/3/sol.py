from utils import *

inp = inp_readall()

muls = re.findall(r"mul\((\d+),(\d+)\)", inp)
print("Part 1:", sum(int(a)*int(b) for a,b in muls))

muls = re.findall(r"mul\((\d+),(\d+)\)|(do\(\)|don't\(\))", inp)

# print(muls)

enabled = True
tot = 0
for a,b,x in muls:
    if x == "do()":
        enabled = True 
    elif x == "don't()":
        enabled = False 
    elif enabled:
        tot += int(a)*int(b)

print("Part 2: ", tot)