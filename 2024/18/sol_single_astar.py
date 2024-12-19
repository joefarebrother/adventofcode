from utils import *

num_b = 12 if is_ex else 1024

points = [P(*ints_in(l)) for l in inp_readlines()]

st = P(0,0)
end = P(6,6) if is_ex else P(70,70)

bounds = Rectangle(st,end)

def search_upto(nps):
    pts = set(points[:nps])
    def adj(p):
        return [np for np in neighbours(p) if np in bounds and np not in pts]
    return FGraph(adj).BFS(st).find(end)

print("Part 1:", search_upto(num_b)[1])

pts_idx = {p:i for i,p in enumerate(points)}
def adj2(p):
    res = {}
    for np in neighbours(p):
        if not np in bounds:
            continue 
        res[np] = 0
        if np in pts_idx:
            res[np] = 1 << (len(points) - pts_idx[np])
    return res 

path = FGraph(adj2).astar(st).path(end)
# print(path)
print([(p,pts_idx[p]) for p in path if p in pts_idx])
pt = min(path, key=lambda p: pts_idx.get(p, math.inf))

print("Part 2:", f"{pt.x},{pt.y}")

# Proof of correctness 

# path is the min path with this adj2 fun by correctness of A*
# to show:
# 1) before adding the point pt, there's a path passing through no obstructions
# 2) after adding point pt, there's no path passing through no obstructions 

# 1) `path` is such a path - all obstructions it passes through are placed after pt by definition of pt being the min index pt along `path`
# 2) suppose p2 did. it passes through no obstructions placed before or equal pt by definition. any obstructions it would pass through are thus placed after pt.
#    however then its cost as a path through the adj2 graph is the sum of unique powers of 2 less than the cost of `pt`, and thus is less than the cost of `path`, contradicting its minimality 

# A* with max instead of + would have the same property