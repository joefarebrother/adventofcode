from utils import *

g = Grid(0)

pos1 = set()
pos2 = set()

for p in set(g.values()):
    if p.upper() in "QWERTYUIOPASDFGHJKLZXCVBNNM1234567890":
        ind = g.indices(p)
        for a,b in itertools.combinations(ind, r=2):
            
            diff = (a-b)
            assert math.gcd(abs(diff.x),abs(diff.y)) == 1

            pos1.add(a+diff)
            pos1.add(b-diff)
            
            px = b
            while px in g:
                pos2.add(px)
                px -= diff

            px = a
            while px in g:
                pos2.add(px)
                px += diff 

print("Part 1:", len(pos1 & set(g.keys())))
print("Part 2:", len(pos2 & set(g.keys())))