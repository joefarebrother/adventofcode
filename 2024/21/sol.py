from utils import *

keypad0 = """789
456
123
 0A"""

keypad1 = """ ^A
<v>"""

def ways_pair(a,b, keypad):
    """Return the (up to) 2 sensible ways to get from a to b, then press A"""
    g = Grid(keypad.split("\n"))
    pa = g.index(a)
    pb = g.index(b)

    
    diff = pa - pb 

    dx = diff.x
    wx = " <>"[sign(dx)]*abs(dx) 
    dy = diff.y
    wy = " ^v"[sign(dy)]*abs(dy)

    res = []
    if g[pa-(dx,0)] != " ":
        res.append(wx+wy+"A")
    if g[pa-(0,dy)] != " ":
        res.append(wy+wx+"A")

    return list(set(res))

# print(ways_pair("<", "A", keypad1))

@cache
def len_best_way(seq, pads):
    """Returns the length of the best way to input the given sequence on `pads` layers of pads"""

    return sum(len_best_way_pair(a,b,pads) for a,b in windows("A"+seq, 2))
    
@cache
def len_best_way_pair(a,b, pads):
    """Returns the length of the best way to get from a to b and press A on `pad` layers of pads"""

    if pads == 0:
        return 1 
    
    if type(pads) == tuple:
        pad, npads = pads 
    else:
        pad, npads = keypad1, pads-1 

    return min(len_best_way(seq, npads) for seq in ways_pair(a,b,pad))

def complexity(line, pads):
    return int(line[:-1]) * len_best_way(line, (keypad0,pads))

inp = inp_readlines()

print("Part 1:", sum(complexity(line, 2) for line in inp))
print("Part 2:", sum(complexity(line, 25) for line in inp))