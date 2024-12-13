from utils import *

g = Grid(0)

def adj(p):
    return [np for np in neighbours(p) if np in g and g[np] == g[p]]

def region(p): 
    return frozenset(FGraph(adj).BFS(p).all_dists().keys())

regs = set()
claimed = set()
for p in g:
    if p not in claimed:
        reg = region(p)
        claimed |= set(reg) 
        regs.add(reg)

def edge_out(p, reg): 
    if p not in reg:
        return 0 
    return sum(1 for np in neighbours(p) if np not in reg)

def perim(reg):
    return sum(edge_out(p,reg) for p in reg)

def price(reg):
    #printx(reg, [g[p] for p in reg])
    return len(reg)*perim(reg)

print("Part 1:", sum(map(price,regs)))

def bulk_perim(reg):
    expected_perim = perim(reg)
    changes = 0 
    seen = set()
    while len(seen) < expected_perim:
        start,sdir = next((p,d) for p in reg for d in neighbours(0) if (p,d) not in seen and p+d not in reg)

        p,dir = start,sdir 
        
        
        while (p,dir) not in seen:
            seen.add((p,dir))
            assert p in reg 
            assert p+dir not in reg, (p,dir,reg)# edge_out(p,reg))
            np = p+dir*Dirs.tR 
            if np in reg:
                p = np 
                if p + dir in reg:
                    p += dir 
                    dir *= Dirs.tL
                    changes += 1
            else:
                dir *= Dirs.tR 
                changes += 1 
        assert (p,dir )== (start,sdir)

    assert len(seen) == expected_perim
    # print(reg, expected_perim, changes)
    return changes
        
def price2(reg):
    printx(reg, [g[p] for p in reg])
    return len(reg)*bulk_perim(reg) 

print("Part 2:", sum(map(price2,regs))) 