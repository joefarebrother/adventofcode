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

last = bin_search(num_b, len(points), lambda n: search_upto(n)[0])
block = points[last]
print("Part 2:", f"{block.x},{block.y}")