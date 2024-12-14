from utils import *

w,h = (11,7) if is_ex else (101,103)

@dataclass
class Robot:
    p: P
    v: P 

    def __init__(self, line):
        px,py,vx,vy = ints_in(line)
        self.p = P(px,py)
        self.v = P(vx,vy)

    def step(self):
        self.p += self.v 
        self.p %= (w,h)

    def quad(self):
        px,py = self.p 
        qs = px<w//2, px>(w//2), py < h//2, py>(h//2) 
        printx(self.p, qs, (qs[0] or qs[1]) and (qs[2] or qs[3]))
        if not ((qs[0] or qs[1]) and (qs[2] or qs[3])):
            return None
        else: return qs[0],qs[2] 


robs = mapl(Robot, inp_readlines())

for _ in range(100):
    for r in robs:
        r.step()

qs = Counter()
for r in robs:
    q = r.quad()
    if q:
        qs[q] += 1 

# print(robs)
# print(qs)

print("Part 1:", math.prod(qs.values()))

def draw():
    g = Grid()
    for r in robs:
        g[r.p] = '#'
    g.draw()

def maybe_tree():
    qs = Counter()
    for r in robs:
        q = r.quad()
        if q:
            qs[q] += 1 
    if abs(qs[(True,True)]+qs[(False,False)]) < 175:
        return True 
    return False
        
time = 100
while time < w*h:
    if is_ex:
        break
    time += 1 
    for r in robs:
        r.step()
    if maybe_tree():
        draw()
        print(time)
        if input("stop?") == "y":
            print("Part 2:", time)
            break
else:
    print("[None found]")

