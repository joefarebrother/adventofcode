from utils import *

g = Grid(0, ints=True)

starts = g.indices(0)
print(starts)

def adj(p):
    return [np for np in neighbours(p) if g[np]==g[p]+1]

gr = FGraph(adj)

def score(start):
    rch = gr.BFS(start).all_dists()
    #print(len(rch))
    #print(start,rch)
    #print([(p,gr[p]) for p in rch])
    return len([p for p in rch if g[p]==9])

@cache
def rating(p):
    if g[p] == 9:
        return 1
    return sum(map(rating,adj(p)))

print("Part 1", sum(map(score,starts)))
print("Part 2", sum(map(rating,starts)))
