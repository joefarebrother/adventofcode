from utils import *

gr = Grid(0, default="#")

start = complex(gr.index("S"))
end = complex(gr.index("E"))

def adj1(p):
    return [complex(np) for np in neighbours(p) if gr[np]!="#"]

g = FGraph(adj1)
dists_end = g.BFS(end).all_dists()
dists_start = g.BFS(start).all_dists()
legit = dists_start[end]

path = g.get_path(end)

assert set(path) == set(dists_start) # This fact is specified in the problem statement, and this solution relies on it

def man_dist(a,b):
    c = a-b 
    return int(abs(c.real) + abs(c.imag))

def time_saved(a, b):
    dist = man_dist(a,b)
    time =  dists_start[a]+dists_end[b]+dist 
    return max(legit-time, 0)

ans = 0
for s in path:
    for d in neighbours(0):
        e = complex(s+2*d)
        if e in dists_end and time_saved(s, e) >= 100:
            ans += 1
print("Part 1:", ans)

ans = 0
ch_thresh = 20
for ai,a in enumerate(path):
    bi = ai+100
    while bi < len(path):
        b = path[bi]

        dist = man_dist(a,b)
        if dist > 20:
            bi += (dist-20)
        else:
            if bi >= ai+120:
                # assert time_saved(a,b) >= 100, (a,b,ai,bi)
                jump = min((20-dist)+1, len(path)-bi)
                ans += jump
                # assert all(time_saved(a, path[bi+j])>=100 and man_dist(a, path[bi+j]) <= 20 for j in range(jump)) 
                bi += jump 
            else:
                if time_saved(a,b) >= 100:
                    ans += 1
                bi += 1

print("Part 2:", ans)