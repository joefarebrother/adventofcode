from utils import *

g = Grid(0)

def adj(p):
    res = []
    for np in neighbours(p):
        if np not in g or g[np] == "#":
            continue 
        # if g[p] in "^v<>" and np-p != Dirs[g[p]]:
        #     continue 
        res.append(np)
    return res 

@cache
def adj_choice(p):
    res = {}
    for np in adj(p):
        d = 1
        use=True
        op = p
        while len(anp := adj(np)) <= 2:
            anp = set(anp)-{op}
            if len(anp) == 0:
                use = (np.y==g.height-1)
                break 
            d += 1
            np,op = only(anp),np
        if use:
            res[np] = d 
    return res

import graphviz
choice_nodes = set(FGraph(adj_choice).BFS(IVec2(1,0)).all_dists().keys())

dot = graphviz.Digraph("gr")
for p in choice_nodes:
    dot.node(str(p))

for p in choice_nodes:
    for np,d in adj_choice(p).items():
        if str(p) < str(np):
            dot.edge(str(p),str(np),str(d))

dot.render("2023/23/gr.gv",format="png")

bits = {}
for i,p in enumerate(choice_nodes):
    bits[p] = 1<<i

@cache
def longest(p, seen):
    if p.y == g.height-1:
        return 0
    
    if not goal_reachable(p,seen):
        return -math.inf
    
    best = -math.inf
    for np,d in adj_choice(p).items():
        if not bits[np] & seen:
            nseen = seen|bits[p]
            best = max(best,d+longest(np,nseen))
            print(p,np,bin(seen),d,best)
    return best

@cache
def goal_reachable(p,seen):
    def adj_mod(p):
        return [np for np in adj_choice(p) if not bits[np] & seen]
    return FGraph(adj_mod).DFS(p).dist(lambda np: np.y == g.height-1) != math.inf 

print("Part 2:", longest(IVec2(1,0),0))

# TODO: alt sol involving astar