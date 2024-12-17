from utils import *

g = Grid(0)

def adj(pd):
    p,d = pd 
    res = {}
    if g[p+d] != "#":
        res[p+d,d] = 1 
    res[p,d*Dirs.tL] = 1000
    res[p,d*Dirs.tR] = 1000 
    return res 

start = only(g.indices("S"))
end = only(g.indices("E"))

gr = FGraph(adj)
best = gr.astar((start,Dirs.E)).find(lambda pd: pd[0]==end)[1]
dists = gr.astar((start,Dirs.E)).all_dists()



print("Part 1:", best) 

gr2 = {pd:adj(pd) for pd in dists}
gr2 = DGraph(gr2).reverse()

rdists = {}
for d in neighbours(0):
    rdists[d] = gr2.astar((end,d)).all_dists()

def on_best_path(p):
    if g[p] != ".":
        return False
    for d in neighbours(0):
        if (p,d) not in dists:
            continue
        if best == dists[p,d] + min(rdists[de][p,d] for de in neighbours(0)):
            return True 
    return False

c = 0      
for p in g:
    if on_best_path(p):
        g[p] = "O"
        c += 1
g.draw()

print("Part 2:", c+2) # +2 bc on_best_path forgor to count S and E