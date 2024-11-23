from utils import *

gr = Grid()
pos = IVec2(0,0)

for line in inp_readlines():
    dr,n,col = line.split(" ")
    for _ in range(int(n)):
        gr[pos] = "#"
        pos += Dirs[dr] 

gr.draw()

class Boundary(Exception):
    pass

def area_at(pt):
    def adj(pt):
        if pt not in gr.bounding_box:
            raise Boundary()
        if gr[pt] is not None:
            return []
        return neighbours8(pt)
    
    return sum(1 for _ in FGraph(adj).BFS(pt))
    
def area_around(pt):
    for np in neighbours8(pt):
        try:
            a = area_at(np)
            if a > 1:
                printx(np,a,gr[np])
                return a
        except Boundary:
            pass

print("Part 1:", area_around(IVec2(0,0)))

verts = [IVec2(0,0)]
pt = IVec2(0,0)

for line in inp_readlines():
    col = re.findall(r'.*\(#(.{6})\)', line)[0]
    dist = int(col[:-1],16)
    dr = [Dirs.R,Dirs.D,Dirs.L,Dirs.U][int(col[-1])]
    pt += dist*dr 
    verts.append(pt)

assert verts[-1]==verts[0]

tot = 0
b = 0
for p1,p2 in windows(verts,2):
    x1,y1 = p1
    x2,y2 = p2

    tot += x1*y2 - y1*x2

    b += int((p1-p2).abs())

A = abs(tot//2)
# picks: A = i + b/2 -1
# want: i + b

i = A+1-b//2

print("Part 2:", b+i)