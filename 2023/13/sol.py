from utils import *

pats = mapl(Grid, inp_groups())

def rowcol(g, n, hor):
    if hor:
        for m in range(g.width()):
            yield g[m,n]
    else:
        for m in range(g.height()):
            yield g[n,m]

def is_refl(g, n, hor):
    dim = g.height() if hor else g.width()
    if n >= dim-1:
        return False
    for i in range(n+1):
        j = 2*n-i+1
        if j < dim:
            #printx(g, n, hor, i, j, list(rowcol(g, i, hor)), list(rowcol(g, j, hor)))
            if list(rowcol(g, i, hor)) != list(rowcol(g, j, hor)):
                return False
        # else:
        #     printx(g,n,hor,i,j,dim)
    printx(g, n, dim, hor, "rettrue")
    return True 

def score(g):
    tot = 0 
    for n in range(max(g.width(), g.height())):
        tot += (n+1)*is_refl(g,n,False) + 100*(n+1)*is_refl(g,n,True)
    return tot

print("Part 1:", sum(map(score,pats)))

def score_smudge(g):
    old = None
    def flip(p):
        g[p] = "#" if g[p] == "." else "."
    for n in range(max(g.width(), g.height())):
        if is_refl(g,n,False):
            old_refl = n,False
            break
        if is_refl(g,n,True):
            old_refl = n,True
            break
    for p in g:
        if old is not None:
            flip(old)
        flip(p)
        old = p 
        for n in range(max(g.width(), g.height())):
            if old_refl != (n,False) and is_refl(g,n,False):
                return (n+1)
            if old_refl != (n,True) and is_refl(g,n,True):
                return 100*(n+1)
            
print("Part 2:", sum(map(score_smudge,pats)))