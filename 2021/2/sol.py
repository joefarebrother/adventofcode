from utils import *

inp = inp_readlines()

x = 0
d = 0
aim = 0
for line in inp:
    cmd, amt = line.split(" ")
    amt = int(amt)
    if cmd == "forward":
        x += amt
        d += amt*aim
    elif cmd == "down":
        aim += amt
    elif cmd == "up":
        aim -= amt

print("Part 1: ", x*aim)
print("Part 2: ", x*d)
