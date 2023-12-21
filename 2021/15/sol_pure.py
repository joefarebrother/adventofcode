from utils import *

inp = Grid(15, ints=True)


def neighbours(pt):
    return [pt+1j**i for i in range(4)]


def path(grid):
    gr = {complex(p): v for p, v in grid.items()}

    def adj(pt):
        return {dp: gr[dp] for dp in neighbours(pt) if dp in gr}
    start = 0
    end = (grid.width-1) + (grid.height-1)*1j

    return FGraph(adj).dijkstra(start).dist(end)


print("Part 1:", path(inp))

grid2 = Grid()

for p in inp:
    for x in range(5):
        for y in range(5):
            nx = p.real + inp.width*x
            ny = p.imag + inp.height*y
            grid2[nx, ny] = mod_inc(inp[p]+x+y, 9)

# grid2.draw(flipy=True)

print("Part 2:", path(grid2))

# sol.py: 9.7s
# sol_pure.py: 5.1s
