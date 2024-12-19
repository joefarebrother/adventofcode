from utils import *

gr = Grid()
num_b = 12 if is_ex else 1024
for line in inp_readlines()[:num_b]:
    x,y = ints_in(line)
    gr[x,y] = "#"

st = P(0,0)
end = P(6,6) if is_ex else P(70,70)

def adj(p):
    return [np for np in neighbours(p) if np in Rectangle(st,end) and not gr[np]=="#"]

print("Part 1:", FGraph(adj).BFS(st).dist(end))

for i,line in enumerate(inp_readlines()[num_b:], start=num_b):
    # print(i, line)
    x,y = ints_in(line)
    gr[x,y] = "#"
    if not FGraph(adj).BFS(st).find(end)[0]:  
        print("Part 2:", f"{x},{y}")
        break 