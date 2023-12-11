from utils import *

g = Grid(0)

cols = set()
rows = set()
gals = set()
for p in g:
    if g[p] == "#":
        gals.add(p)
        cols.add(p.x)
        rows.add(p.y)

expanded_rows = set(g.bounding_box.yrange()) - rows
expanded_cols = set(g.bounding_box.xrange()) - cols

adjusted_gals = set()
for p in gals:
    x,y = p 
    nx = x + ((100 if is_ex else 1000000)-1)* len([ex for ex in expanded_cols if ex < x])
    ny = y + ((100 if is_ex else 1000000)-1)* len([ey for ey in expanded_rows if ey < y])
    adjusted_gals.add(IVec2(nx,ny))

tot_dist = sum(man_dist(p1, p2) for p1,p2 in itertools.product(adjusted_gals, adjusted_gals) if p1!=p2)
print("Part 2:", tot_dist//2)