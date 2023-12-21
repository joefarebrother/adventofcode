from utils import *

g = Grid(0, y_is_down=True)
Dirs.flipy()

start = only([p for p,x in g.items() if x == "S"])

def connections(p):
    pipe = g[p]
    if pipe == "." or pipe == "S":
        return ()
    if pipe == "-":
        return p+Dirs.L,p+Dirs.R
    if pipe == "|":
        return p+Dirs.U,p+Dirs.D
    if pipe == "F":
        return p+Dirs.D,p+Dirs.R
    if pipe == "J":
        return p+Dirs.L,p+Dirs.U 
    if pipe == "7":
        return p+Dirs.L,p+Dirs.D 
    if pipe == "L":
        return p+Dirs.U,p+Dirs.R 
    raise Exception("?")
    
def find_loop(p):
    prev = start 
    l = [p]
    while p != start:
        con = connections(p)
        if prev not in con:
            return None 
        nxt = only(x for x in con if x != prev)
        l.append(nxt)
        prev,p = p,nxt
    return l

for p in neighbours(start):
    loop = find_loop(p)
    if loop:
        break 

print("Part 1:", len(loop)//2)

loop_vert = set()
for x,y in windows(loop+[loop[0]], 2):
    if x-y == (0,1):
        loop_vert.add(x)
    if y-x == (0,1):
        loop_vert.add(y)
loop = set(loop)

area = 0
for y in range(g.height):
    inside = False 
    for x in range(g.width):
        p = IVec2(x,y)
        if p in loop_vert:
            inside ^= True 
        if p not in loop:
            area += inside
            if inside:
                g[p] = block_char

# g.draw()

print("Part 2:", area)
