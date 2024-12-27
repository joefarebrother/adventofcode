from utils import *

grs = mapl(Grid,inp_groups())

grs = [set(gr.indices("#")) for gr in grs]

def fit(a,b):
    return not a&b 

ans = 0
for a,b in itertools.combinations(grs,r=2):
    if fit(a,b):
        ans += 1

print(ans)