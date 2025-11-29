from utils import *

@dataclass(frozen=True)
class Vec:
    x:int
    y:int
    z:int 

    def __add__(self,other):
        return Vec(self.x+other.x,self.y+other.y,self.z+other.z)
    
    def dist(self):
        return abs(self.x)+abs(self.y)+abs(self.z)
    
@dataclass
class Particle:
    p:Vec 
    v:Vec 
    a:Vec 

    def step(self):
        self.v += self.a
        self.p += self.v

def part(line):
    i = ints_in(line)
    print(i)
    return Particle(p=Vec(*i[:3]),v=Vec(*i[3:6]),a=Vec(*i[6:9])) 
 
inp = mapl(part, inp_readlines())

for _ in range(10000):
    for p in inp:
        p.step()
    by_pos = defaultdict(list)
    for p in inp:
        by_pos[p.p].append(p)
    ninp = []
    for l in by_pos.values():
        if len(l) == 1:
            ninp += l 
    inp = ninp

dists = [p.p.dist() for p in inp] 

#print("Part 1:", min(range(len(dists)), key=lambda i: dists[i]))
print("Part 2:", len(inp))