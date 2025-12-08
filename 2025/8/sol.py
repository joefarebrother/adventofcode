from utils import *

def dist_sq(p1,p2):
    return sum((a-b)*(a-b) for a,b in zip(p1,p2))

inp=  inp_readlines()

pts = mapl(tuple,mapl(ints_in, inp))

cons = 10 if is_ex else 1000

pairs = sorted(itertools.combinations(pts,2), key=lambda xy: dist_sq(xy[0],xy[1]))

sets = DisjointSets(pts)

def connect(p1,p2):
    sets.union(p1,p2)

for p1,p2 in pairs[:cons]:
    printx(p1,p2)
    connect(p1,p2)

#printx(sets)

uniqs = sets.uniq_sets()

top = sorted(uniqs,key=len,reverse=True)
printx(top)

print("Part 1:", math.prod(map(len, top[:3])))

def all_connected():
    return len(sets.get_set(pts[0])) == len(pts)

for p1,p2 in pairs[cons:]:
    connect(p1,p2)
    if all_connected():
        print("Part 2:", p1[0]*p2[0])
        break
