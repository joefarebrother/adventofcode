from utils import *

tiles = [P(*ints_in(r)) for r in inp_readlines()]

print("Part 1:", max(len(Rectangle(a,b)) for a,b in it.combinations(tiles,2)))

lines = list(zip(tiles, tiles[1:]+[tiles[0]]))

vert_lines = sorted([(a,b) for (a,b) in lines if a.x == b.x], key=lambda a: a[0].x)

def ori(l):
    return sign(l[0].y - l[1].y)

poly = CuboidSet()

for l in vert_lines:
    if ori(l) == ori(vert_lines[0]):
        span = Cuboid([(l[0].x, math.inf), (l[0].y, l[1].y)])
        poly |= span 
    else:
        shadow = Cuboid([(l[0].x+1, math.inf), (l[0].y, l[1].y)])
        poly -= shadow

print(poly.volume(), len(poly.cubs))

rects = sorted([Rectangle(a,b) for a,b in it.combinations(tiles,2)], key=len, reverse=True)

print("sorted", len(rects))
def valid(r):
    if any(p not in poly for p in r.corners()):
        return False
    return (poly & r).volume() == len(r)

print("Part 2:", next(len(r) for r in rects if valid(r))) 