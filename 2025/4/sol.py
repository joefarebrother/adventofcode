from utils import *

gr = Grid(0)
bb = gr.bounding_box

def acc(p):
    return gr[p] == "@" and sum(1 for np in neighbours8(p) if gr[np] == "@") < 4

print("Part 1:", sum(1 for p in gr.bounding_box if acc(p)))

def all_acc():
    return set(p for p in bb if acc(p))

tot = 0
while True:
    rem = all_acc()
    tot += len(rem)
    if len(rem) == 0:
        break 
    for p in rem:
        gr[p] = "."

print("Part 2:", tot)

# 287th