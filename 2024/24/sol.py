from utils import *

wires0,gates0 = inp_groups()

wires_vals = defaultdict(int)

for w in wires0:
    n,v = w.split(": ")
    wires_vals[n] = bool(int(v))

gates = {}

for g in gates0:
    print(g)
    a,op,b,out = match(r"(...) ([A-Z]+) (...) -> (...)", g)
    gates[out] = (op, a, b)

@cache
def ev(g):
    if g in wires_vals:
        return wires_vals[g]
    
    op,a,b = gates[g]
    a,b = ev(a), ev(b)

    return {"AND": a&b, "OR":a|b, "XOR":a^b}[op]

zs = {w:ev(w) for w in wires_vals|gates if w[0] == "z"}
val = "".join(str(int(zs[w])) for w in sorted(zs, reverse=True))

for w in sorted(wires_vals|gates):
    print(f"{w}: ", ev(w))
print("Part 1:", int(val,2))

import graphviz as gv
dot = gv.Digraph()

for a in wires_vals|gates:
    if a in wires_vals:
        lab = f"in {a} {int(wires_vals[a])}"
    else:
        lab = f"{gates[a][0]} {a}"
    dot.node(a,lab)

for g,(op,a,b) in gates.items():
    dot.edge(a, g, label=a)
    dot.edge(b, g, label=b)
    if g[0] == "z":
        dot.node(g+"out", g+"out")
        dot.edge(g, g+"out", label=g)

# dot.render("2024/24/in.gv", format="png")

for z in zs:
    if gates[z][0] != "XOR" or not any(gates.get(a, " ")[0] == "XOR" for a in gates[z][1:]):
        print(z, gates[z])

# ands = {}
# xors = {}
# for i in range(44):
#     for g,(op,a,b) in gates.items():
#         a,b = sorted((a,b))
#         if a == f"x{i:02}" or b == f"y{i:02}":
#             if (op,a,b) not in [("XOR",f"x{i:02}",f"y{i:02}"),("AND",f"x{i:02}",f"y{i:02}")]:
#                 print(g,(op,a,b))
#             else:
#                 if op[0] == "XOR":
#                     xors[i] = g 
#                 else:
#                     ands[i] = g 

# for g,(op,a,b) in gates.items():
#     if op == "OR":
#         if gates[a][0] != "AND" or gates[b][0] != "AND":
#             print(g, (op,a,b))



swap = (("z08", "cdj"), ("z32", "gfm"), ("z16", "mrb"), ("qjd", "dhm"))

swap = sorted([a for b in swap for a in b])

print("Part 2:", ",".join(swap))