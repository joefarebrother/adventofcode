from utils import *

inp = Grid(0)

start = only(p for p, s in inp.items() if s == "S")
end = only(p for p, s in inp.items() if s == "E")


def height(c):
    if c == "S":
        return 0
    if c == "E":
        return 25
    return ord(c)-ord("a")


def adj(p1):
    """Inverse graph (i.e. searching backwards from the end point) handles both parts"""
    for p in neighbours(p1):
        if p in inp:
            if height(inp[p]) + 1 >= height(inp[p1]):
                yield p


gr = FGraph(adj)
dist = gr.BFS(end).dist(start)
# path = gr.get_rev_path(end)
# for p0, p1 in windows(path, 2):
#     print(p0, p1, inp[p0], inp[p1], height(inp[p0])-height(inp[p1]))

print("Part 1:", dist)


st, best = gr.BFS(end).find(lambda s: inp[s] == "a")
# path = gri.get_rev_path(st)
# for p0, p1 in windows(path, 2):
#     print(p0, p1, inp[p0], inp[p1], height(inp[p0])-height(inp[p1]))

print("Part 2:", best)
