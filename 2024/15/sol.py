from utils import *

gr, instrs = inp_groups()
gr = Grid(gr)

rob = only(gr.indices("@"))

def push(p,d):
    if gr[p+d] == "#":
        return False 
    if gr[p+d] == "O":
        if not push(p+d,d):
            return False
    assert gr[p+d] == ".", (gr[p+d], p+d)

    gr[p+d],gr[p] = gr[p],"."
    return True 

for instr in "".join(instrs):
    d = Dirs[instr]
    if push(rob,d):
        rob += d 
        #gr.draw()

ans = 0 
for p in gr.indices("O"):
    ans += 100*p.y + p.x

print("Part 1:", ans)

ogr, instrs = inp_groups()

ogr = Grid(ogr)

gr = Grid()
for p,c in ogr.items():


    # If the tile is #, the new map contains ## instead.
    # If the tile is O, the new map contains [] instead.
    # If the tile is ., the new map contains .. instead.
    # If the tile is @, the new map contains @. instead.

    np1 = P(2*p.x,p.y)
    np2 = P(2*p.x+1,p.y)
    
    nc = {"#":"##","O":"[]",".":"..","@":"@."}[c]
    gr[np1], gr[np2] = nc

gr.draw()

rob = only(gr.indices("@"))

def can_push(p,d):
    #printx(p,d, gr[p+d], depth)
    if gr[p+d] == "#":
        return False 
    if gr[p+d] == "O":
        if not push(p+d,d):
            return False
    if gr[p+d] in "[]":    
        od = (-1,0) if gr[p+d]=="]" else (1,0)

        if gr[p+d+od] not in "[]": # disconnected box; must be in the middle of a push
            return can_push(p+d,d)
        if od == d:
            return can_push(p+d+od,d)
        elif od == -d:
            return can_push(p+d,d)
        else:
            return(can_push(p+d+od,d)) and can_push(p+d,d)
        

    return True 

def push2(p,d):
    # print(p,d)
    if not can_push(p,d):
        return False 
    if gr[p+d] in "[]":
        od = (-1,0) if gr[p+d]=="]" else (1,0)
        #if gr[p+d+od] in "[]":
        if od != -d:
            assert push2(p+d+od,d)
        assert push2(p+d,d)
    
    assert gr[p+d] == ".", (gr[p+d], p+d)

    #print(p,p+d,gr[p]) 
    gr[p+d],gr[p] = gr[p],"."
    return True 


for instr in "".join(instrs):
    d = Dirs[instr]
    if push2(rob,d):
        rob += d 
        #gr.draw()
    # assert gr[rob] == "@", (rob, gr[rob])
    # for p in gr.indices("["):
    #     assert gr[p+(1,0)] == "]"
    

ans = 0 
for p in gr.indices("["):
    ans += 100*p.y + p.x

print("Part 2:", ans)

