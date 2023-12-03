from utils import *

g = Grid(0, default=".")

parts = []
digs = "1234567890"
gears = defaultdict(list)

for p, c in g.items():
    if c in digs and g[p-(1,0)] not in digs:
        n = ""
        adj = []
        adj.append(p-(1,0))
        adj.append(p-(1,1))
        adj.append(p-(1,-1))
        for i in range(g.width()):
            if (nc := g[p+(i,0)]) in digs:
                n += nc
                adj.append(p+(i,1))
                adj.append(p+(i,-1))
            else:
                break 
        adj.append(p+(len(n),0))
        adj.append(p+(len(n),1))
        adj.append(p+(len(n),-1))
        #print(n, adj)

        for a in adj:
            if g[a] == "*":
                gears[a].append(int(n))

        if any(g[a] != "." and g[a] not in digs for a in adj):
            parts.append(int(n))

#print(parts)
print("Part 1:", sum(parts))

tot = 0
for g in gears.values():
    if len(g) == 2:
        tot += math.prod(g)
print("Part 2:", tot)