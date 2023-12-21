from utils import *

g = Grid(0)

def adj(p):
    return [np for np in neighbours(p) if (np in g and g[np] != "#")]

gr = FGraph(adj)

start = only(p for p,v in g.items() if v == "S")

dists = gr.BFS(start).all_dists()

target_steps = 6 if is_ex else 64 

def reachable(p):
    return p in dists and dists[p] <= target_steps and (dists[p]-target_steps)%2==0 

print("Part 1:", sum(1 for p in g if reachable(p)))

# def adj2(p):
#     for np in neighbours(p):
#         x,y = np 
#         x %= g.width
#         y %= g.height
#         np = IVec2(x,y)
#         if g[np] != "#":
#             yield np 
        

# dists2 = FGraph(adj2).BFS(start).all_dists()

metalen = 4

def adj_expanded3(p):
    gp,mp = p 
    res = []
    for ngp in neighbours(gp):
        x,y = ngp 
        mx,my = mp 
        mx += x//g.width
        my += y//g.height
        x %= g.width
        y %= g.height
        ngp = IVec2(x,y)
        nmp = IVec2(mx,my)
        if g[ngp] != "#" and nmp in Rectangle((-metalen,-metalen),(metalen,metalen)):
            res.append((ngp,nmp)) 
    return res

dists_expanded = FGraph(adj_expanded3).BFS((start,IVec2(0,0))).all_dists()

# dists_expanded_centre = {}
# diffs = {}
# for p in g:
#     if g[p] == "#":
#         continue 
#     dists_expanded_centre[p] = dists_expanded[p,(0,0)]
#     diffs[p] = dists_expanded[p,(0,0)] - dists[p]

# print(diffs)

# for p in g:
#     a = adj(p)
#     b = adj_expanded3((p,IVec2(0,0)))
#     assert len(a) == len(b), (p,a,b)

# exit()

for p in g:
    if p not in dists:
        continue 

    loc_dists = {}
    for mp in Rectangle((-metalen,-metalen),(metalen,metalen)):
        loc_dists[mp] = dists_expanded[p,mp]

    loc_vdiffs = {}
    for mp in Rectangle((-metalen,-metalen),(metalen,metalen-1)):
        loc_vdiffs[tuple(mp)] = loc_dists[mp]-loc_dists[mp+(0,1)]

    loc_hdiffs = {}
    for mp in Rectangle((-metalen,-metalen),(metalen-1,metalen)):
        loc_hdiffs[tuple(mp)] = loc_dists[mp]-loc_dists[mp+(1,0)]

    print(p, "\nv", loc_vdiffs, "\nh", loc_hdiffs)

    for x in irange(-metalen,metalen):
        col = {(x,y):v for (x1,y),v in loc_vdiffs.items() if x == x1}
        #assert len(set(col.values())) <= 3, (p,"col",x,col)
        coll = list(col.values())
        assert (abs(coll[0]) == g.width and abs(coll[-1]) == g.width), ("col",x,col,coll)

    for y in irange(-metalen,metalen):
        row = {(x,y):v for (x,y1),v in loc_hdiffs.items() if y == y1}
        #assert len(set(col.values())) <= 3, (p,"row",y,row)
        rowl = list(row.values())
        assert (abs(rowl[0]) == g.width and abs(rowl[-1]) == g.width), ("row",y,row,rowl)

# turns out loc_vdiff/hdiff is gridsize
    
target_steps = 5000 if is_ex else 26501365
def good_combinations(dist):
    # on a grid with metacoords (x,y), dist to p is 131*(x')+131*(y')+dist_at(1,1) (for quadrant 1: x',y'>=0 = x+1)
    # = 131* (x+y)+dist_at(1,1)
    # how many of these are "good"?
    # good if target-dist is nonneg and even 
    # looking for sums of "good" x,y
    # "good" s if 131*s + dist is "good"
    # => how many s st 131*s is small and correct parity?
    # => (target-dist)//131 for size

    # for given s, how many x/s? it's s+1
    # sum of n odds is n^2, sum of n evens is n(n-1)
    

    size = g.width
    target = target_steps - dist # what i'm trying to make 131*s be less than and even
    if target < 0:
        return 0

    rngmax = target // size 
    print("quad",rngmax, dist)
    if target%2 == 1:
        odds = (rngmax+1)//2
        return odds*(odds+1)
    else:
        evens = rngmax//2+1
        return evens*evens
    
def good_combinations_linear(dist):
    # same but in just 1 dir 
    size = g.width
    target = target_steps - dist

    rngmax = target // size 
    if target < 0:
        return 0
    # if rngmax>0:
    #     print("line",rngmax, dist)

    if target%2 == 1:
        # num odd numbers up to rngmax
        return (rngmax+1)//2
    else:
        return rngmax//2+1

def ways_quadrant(p,q):
    return good_combinations(dists_expanded[p,q])

def ways_linear(p,q):
    return good_combinations_linear(dists_expanded[p,q])

def ways_centre(p,q):
    return int((dists_expanded[p,q]-target_steps)%2 == 0 and dists_expanded[p,q] <= target_steps)

def ways(p):
    if p not in dists:
        return 0
    
    res = 0
    for q in Rectangle((-metalen,-metalen),(metalen,metalen)):
        qx,qy = q
        if abs(qx) == metalen and abs(qy) == metalen:
            res += ways_quadrant(p,q)
        elif abs(qx) == metalen or abs(qy) == metalen:
            res += ways_linear(p,q)
        else:
            res += ways_centre(p,q)
    return res

print("Part 2:", sum(ways(p) for p in g))