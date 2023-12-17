from utils import *

inp = Grid(0)
Dirs.flipy()

def adj(node):
    p, d, c = node 
    if p == None:
        return {(IVec2(0,0),Dirs.R,0):0, (IVec2(0,0),Dirs.D,0):0}
    res = {}
    for np in neighbours(p):
        if np not in inp:
            continue
        if np-p == -d:
            continue
        if np-p == d:
            if c < 2:
                res [(np, d, c+1)]=int(inp[np])
        else:
            res[(np, np-p, 0)]=int(inp[np])
    return res

gr = FGraph(adj)
start = (None,0,0)
# print("Part 1:", gr.dijkstra(start).dist(lambda n: n[0] == (inp.width()-1, inp.height()-1)))

def adj2(node):
    p, d, c = node 
    res = {}
    if p == None:
        return {(IVec2(0,0),Dirs.R,-1):0, (IVec2(0,0),Dirs.D,-1):0}
    for np in neighbours(p):
        if np not in inp:
            continue
        if np-p == -d:
            continue
        if np-p == d:
            if c < 9:
                res [(np, d, c+1)]=int(inp[np])
        else:
            if c >= 3:
                res[(np, np-p, 0)]=int(inp[np])
    return res

gr = FGraph(adj2)
print("Part 2:", gr.dijkstra(start).dist(lambda n: n[0] == (inp.width()-1, inp.height()-1) and n[2]>=3))