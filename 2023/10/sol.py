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

def is_int(x):
    return x == int(x)

class Boundary(Exception):
    pass

def adj(p):
    x,y = p
    if is_int(x) and is_int(y) and p not in g:
        raise Boundary()
    
    ns = [(x+0.5,y), (x-0.5,y), (x,y+0.5), (x,y-0.5)]
    return [p1 for p1 in ns if not p1 in loop_halfints]

loop_halfints = set()
for p1,p2 in windows(loop+[loop[0]], 2):
    loop_halfints.add(tuple(p1))
    loop_halfints.add(tuple(p2))
    x1,y1 = p1 
    x2,y2 = p2 
    loop_halfints.add(((x1+x2)/2, (y1+y2)/2))

loop = set(loop)

def area(p):
    res = FGraph(adj=adj).BFS(p)
    n = 0

    sg = {}
    for x,y in loop_halfints:
        sg[2*x, 2*y] = "*"
    for p,s in g.items():
        if p in loop:
            x,y = p
            sg[2*x,2*y] = s 

    try:
        for (x,y),_d in res:
            sg[2*x, 2*y] = "."
            if is_int(x) and is_int(y):
                assert IVec2(x,y) not in loop_halfints, (x,y)
                n += 1
                sg[2*x,2*y] = block_char
        sg = Grid(sg, y_is_down=True)
        # sg.draw()
        return n
    except Boundary:
        return 0

for (x,y) in neighbours8(0):
    sx,sy = start 
    a = area((sx+x/2, sy+y/2))
    if a > 0:
        print("Part 2:", a)
        break