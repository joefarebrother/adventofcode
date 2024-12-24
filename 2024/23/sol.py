from utils import *

gr = defaultdict(list)

for line in inp_readlines():
    a,b = line.split("-")
    gr[a].append(b)
    gr[b].append(a)

tcliques = set()
for a in gr:
    if a[0] == "t":
        for b,c in it.combinations(gr[a], r=2):
            if c in gr[b]:
                tcliques.add(frozenset((a,b,c)))

print("Part 1:", len(tcliques))

def is_clique(xs):
    return all(a in gr[b] for a,b in it.combinations(xs, r=2))

maxclique = {1,2,3}
for a in gr:
    for r in range(len(maxclique), 13):
        for cl in it.combinations(gr[a], r=r):
            if is_clique(cl):
                maxclique = set(cl)|{a}
        else:
            break 

print("Part 2:", ",".join(sorted(maxclique)))