from utils import *

mirs = Grid(0)
Dirs.flipy()

def prop(b):
    p,d = b 
    elem = mirs[p]
    if elem == ".":
        return [(p+d, d)]
    if elem in "|-":
        if (elem == "|" and IVec2(d).x == 0) or (elem == "-" and IVec2(d).y == 0):
            return [(p+d, d)]
        nd1 = d*Dirs.tL
        nd2 = d*Dirs.tR
        return [(p+nd1,nd1),(p+nd2,nd2)]
    if elem in "/\\":
        nd = {"\\":{Dirs.U:Dirs.L,Dirs.L:Dirs.U,Dirs.R:Dirs.D,Dirs.D:Dirs.R},"/":{Dirs.U:Dirs.R,Dirs.R:Dirs.U,Dirs.L:Dirs.D,Dirs.D:Dirs.L}}[elem][d]
        return [(p+nd, nd)] 
    raise Exception("???")

def from_edge(b):
    beam = {b}
    seen_beem = {b}

    while beam:
        new_beam = set()
        for b in beam:
            printx("beam", b)
            for nb in prop(b):
                printx("check:", nb)
                if nb[0] in mirs and nb not in seen_beem:
                    printx("added")
                    new_beam.add(nb)
                    seen_beem.add(nb)
        beam = new_beam

    printx(seen_beem)
    energised = {p for p,d in seen_beem}

    if is_ex:
        mirs2 = Grid(mirs)
        for p in energised:
            mirs2[p] = "#"
        mirs2.draw()

    return len(energised)

print("Part 1:", from_edge((IVec2(0,0), Dirs.R))) 

edges = [(IVec2(x,0),Dirs.D) for x in range(mirs.width)] + [(IVec2(x,mirs.height-1),Dirs.U) for x in range(mirs.width)]+ [(IVec2(0,y),Dirs.R) for y in range(mirs.height)] + [(IVec2(mirs.width-1,y),Dirs.L) for y in range(mirs.height)]
print("Part 2:", max(from_edge(e) for e in edges))