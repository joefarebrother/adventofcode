from utils import *

grs = mapl(Grid,inp_groups())

def heights(g: Grid):
    return [sum(1 for p in g.indices("#") if p.x==x) for x in g.bounding_box.xrange()]

def fit(a,b):
    if a[0,0]==b[0,0]:
        return False 
    ha = heights(a)
    hb = heights(b)
    # a.draw()
    # print(ha)
    # b.draw()
    # print(hb)
    s = [c+d for c,d in zip(ha,hb)]
    # print(ha,hb, s)
    return all(t <= a.height for t in s)

ans = 0
for a,b in itertools.combinations(grs,r=2):
    if fit(a,b) or fit(b,a):
        ans += 1

print(ans)