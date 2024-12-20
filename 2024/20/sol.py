from utils import *

gr = Grid(0, default="#")

start = only(gr.indices("S"))
end = only(gr.indices("E"))

dots = mapl(complex, gr.indices(".")) + [start,end]

def adj1(p):
    return [np for np in neighbours(p) if gr[np]!="#"]

g = FGraph(adj1)
dists_end = g.BFS(end).all_dists()
dists_start = g.BFS(start).all_dists()
legit = dists_start[end]

def cheat(p,np):
    if np not in dists_end:
        return 0
    de = dists_end[np]
    return max([0]+[legit-(dists_start[sp]+de+2) for sp in neighbours(p) if sp in dists_start])


ans = 0 
for p in gr.indices("#"):
    for np in neighbours(p):
        if cheat(p,np)>=100:
            ans += 1

print("Part 1:", ans)

def cheat2(p1,p2):
    len_ch = man_dist(p1,p2) 
    time = dists_start[p1]+dists_end[p2]+len_ch 
    if len_ch <= 20 and time < legit:
        return legit-time
    return 0 

ans = 0
for p in gr:
    if gr[p] != "#":
        for dp in Rectangle((-20,-20),(20,20)):
            p2 = p+dp 
            if gr[p2] != "#":
                if cheat2(p,p2) >= 100:
                    ans += 1

print("Part 2:", ans)