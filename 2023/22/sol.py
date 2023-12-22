from utils import *

cubs = []
for line in inp_readlines():
    x1,y1,z1,x2,y2,z2= ints_in(line)
    cubs.append(Cuboid([(x1,x2),(y1,y2),(z1,z2)]))

cubs = sorted(cubs, key=lambda c: c.dims[-1].start)

fallen = []
supp_gr = defaultdict(list)
rev_sup_gr = defaultdict(list)

for c in cubs:
    stacks = [f for f in fallen if f.project(2)&c.project(2)]
    maxz = max([0]+[f.dims[2].endx for f in stacks])
    support = [f for f in stacks if f.dims[2].endx == maxz]
    fall = c.shift((0,0,maxz-c.dims[2].start))
    #print(c,maxz,fall,support)
    fallen.append(fall)
    supp_gr[fall] = support 
    for s in support:
        rev_sup_gr[s].append(fall)

for f1,f2 in itertools.combinations(fallen, r=2):
    assert not (f1&f2), (f1,f2)

tot = 0 
for f in fallen:
    supporting = rev_sup_gr[f]
    print(f, supporting)
    if all(len(supp_gr[c]) >= 2 for c in supporting):
        tot += 1

print("Part 1:", tot)

tot = 0
rev_sup_gr_gr = DGraph(rev_sup_gr)
for f in fallen:
    falls = set([f])
    all_sup = rev_sup_gr_gr.BFS(f).all_dists().keys()
    all_sup = sorted(all_sup,key=lambda c: c.dims[2].endx)
    for s in all_sup:
        if all(sup in falls for sup in supp_gr[s]):
            falls.add(s)
    printx(f, falls)
    tot += len(falls)-1 

print("Part 2:", tot)
