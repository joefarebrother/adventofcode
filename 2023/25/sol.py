from utils import *

gr = defaultdict(list)
for line in inp_readlines():
    l = line.split(" ")
    a = l[0][:-1]
    bs = l[1:]
    for b in bs:
        gr[a].append(b)
        gr[b].append(a)

import graphviz
dot = graphviz.Digraph()

for a in gr:
    dot.node(a,a)

for a,bs in gr.items():
    for b in bs:
        #if str(a) < str(b):
            dot.edge(a,b)

if is_ex:
    dot.render("2023/25/ex.gv", format="png")

f = {}
for a in gr:
    for b in gr[a]:
        f[a,b] = 0
        f[b,a] = 0

def adj_f(a):
    return [b for b in gr[a] if 1 - f[a,b] > 0]

src = "jqt" if is_ex else "nmp" # found with graphviz
tgt = "rsh" if is_ex else "mvz"
# ford-fulk
while True:
    gf = FGraph(adj_f)
    n,d = gf.BFS(src).find(tgt)
    if n == None:
        break 
    p = gf.get_rev_path(n)
    for b,a in windows(p,2):
        f[a,b] += 1
        f[b,a] -= 1

gf = FGraph(adj_f)
cc1 = len(gf.BFS(src).all_dists())
cc2 = len(gr) - cc1

print("Part 1:", cc1, cc2, cc1*cc2)