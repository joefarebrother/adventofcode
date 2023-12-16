from utils import *

def hash_(x):
    res = 0
    for ch in x:
        res = ((res+ord(ch))*17)%256 
    return res

inp = inp_readall().replace("\n", "").split(",")

print("Part 1:", sum(hash_(x) for x in inp))

boxes = [{} for _ in range(256)]

for l in inp:
    if l.endswith("-"):
        l = l[:-1]
        if l in boxes[hash_(l)]:
            del boxes[hash_(l)][l]
    else:
        l,x = l.split("=")
        boxes[hash_(l)][l] = int(x)

tot = 0
for bi,b in enumerate(boxes):
    for li,(l,ll) in enumerate(b.items()):
        tot += (bi+1)*(li+1)*ll

print("Part 2:", tot)