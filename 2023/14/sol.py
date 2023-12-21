from utils import *

g = Grid(0)

rounded = {p for p in g if g[p] == "O"}
square = {p for p in g if g[p] == "#"}

def by_col(ps):
    cols = defaultdict(list)
    for p in ps:
        cols[p.x].append(p)
    return cols

def by_row(ps):
    rows = defaultdict(list)
    for p in ps:
        rows[p.y].append(p)
    return rows


def load(rounded): 
    tot = 0
    for p in rounded:
        tot += g.height-p.y
    return tot
    

def roll_north(rounded):
    rc = by_col(rounded)
    sc = by_col(square)
    new_rounded = set()

    for c in rc:
        rcol = set(rc[c])
        scol = set(sc[c])
        new_rcol = set()
        for p in sorted(rcol, key=lambda p:p.y):
            y = max([0]+[s.y+1 for s in scol if s.y < p.y] + [s.y+1 for s in new_rcol if s.y < p.y])
            new_rcol.add(IVec2(p.x,y))
        new_rounded |= new_rcol

    assert len(new_rounded) == len(rounded), ("n",rounded, new_rounded)
    return new_rounded

def roll_south(rounded):
    rc = by_col(rounded)
    sc = by_col(square)
    new_rounded = set()

    for c in rc:
        rcol = set(rc[c])
        scol = set(sc[c])
        new_rcol = set()
        for p in sorted(rcol, key=lambda p:p.y, reverse=True):
            y = min([g.height-1]+[s.y-1 for s in scol if s.y > p.y] + [s.y-1 for s in new_rcol if s.y > p.y])
            #printx(y)
            new_rcol.add(IVec2(p.x,y))
        new_rounded |= new_rcol

    assert len(new_rounded) == len(rounded), ("s",rounded, new_rounded)
    return new_rounded

def roll_west(rounded):
    rc = by_row(rounded)
    sc = by_row(square)
    new_rounded = set()

    for c in rc:
        rrow = set(rc[c])
        srow = set(sc[c])
        new_rrow = set()
        for p in sorted(rrow, key=lambda p:p.x):
            x = max([0]+[s.x+1 for s in srow if s.x < p.x] + [s.x+1 for s in new_rrow if s.x < p.x])
            #printx(x)
            new_rrow.add(IVec2(x,p.y))
        new_rounded |= new_rrow

    assert len(new_rounded) == len(rounded), ("w",rounded, new_rounded)
    return new_rounded

def roll_east(rounded):
    rc = by_row(rounded)
    sc = by_row(square)
    new_rounded = set()

    for c in rc:
        rrow = set(rc[c])
        srow = set(sc[c])
        new_rrow = set()
        for p in sorted(rrow, key=lambda p:p.x, reverse=True):
            x = min([g.width-1]+[s.x-1 for s in srow if s.x > p.x] + [s.x-1 for s in new_rrow if s.x > p.x])
            #printx(x)
            new_rrow.add(IVec2(x,p.y))
        new_rounded |= new_rrow

    assert len(new_rounded) == len(rounded), ("e",rounded, new_rounded)
    return new_rounded

def roll_all(rounded):
    rounded = roll_north(rounded)
    rounded = roll_west(rounded)
    rounded = roll_south(rounded)
    rounded = roll_east(rounded)
    return rounded 

print("Part 1:", load(roll_north(rounded)))

seen = {}
i = 0
while i < 1000000000:
    frounded = frozenset(rounded)
    if frounded in seen:
        lasti = seen[frounded]
        per = i-lasti 
        rep = (1000000000-i)//per 
        printx(i,lasti,per,rep,i+per*rep)
        i += per*rep
    seen[frounded] = i
    rounded = roll_all(rounded)
    i += 1
    if i <= 3:
        printx(i)
        if is_ex:
            ng = Grid(g)
            for p in ng:
                if ng[p] == "O":
                    ng[p] = "."
            for p in rounded:
                ng[p] = "O"
            ng.draw()

print("Part 2:", load(rounded))