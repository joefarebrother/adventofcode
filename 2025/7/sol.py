from utils import *

gr = Grid(0)

st = gr.index("S")

tach = set(st)
splits = 0 

for _ in range(gr.height):
    ntach = set()
    for t in tach:
        nt = t+Dirs.D 
        if gr[nt] == "^":
            splits += 1
            ntach |= {nt+Dirs.L,nt+Dirs.R}
        else:
            ntach |= {nt}
    tach = ntach

print("Part 1:", splits)

@cache 
def t_from(p):
    if p.y >= gr.height:
        return 1 
    if gr[p] == "^":
        return t_from(p+Dirs.L) + t_from(p+Dirs.R)
    else:
        return t_from(p+Dirs.D)
    
print("Part 2:", t_from(st))