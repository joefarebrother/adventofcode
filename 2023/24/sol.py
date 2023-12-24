from utils import *
import sympy

@dataclass(unsafe_hash=True)
class Vector:
    data: tuple

    def __init__(self, data):
        self.data = tuple(data)

    def __getitem__(self, i):
        return self.data[i]

    def __add__(self, other):
        assert len(self.data) == len(other.data), (self, other)
        return Vector(self[i] + other[i] for i in range(len(self.data)))

    def __sub__(self, other):
        return Vector(self[i] - other[i] for i in range(len(self.data)))
    
    def __mul__(self, other):
        return Vector(self[i]*other for i in range(len(self.data)))
    
    __rmul__ = __mul__

    def man_dist(self, other):
        return sum(abs(self[i]-other[i]) for i in range(len(self.data)))

hails_xy = []
hails_xyz = []
for line in inp_readlines():
    x,y,z,vx,vy,vz = ints_in(line)
    hails_xy.append((Vector((x,y)),Vector((vx,vy))))
    hails_xyz.append((Vector((x,y,z)),Vector((vx,vy,vz))))
                    
def collide(h1,h2):
    p1,v1 = h1 
    p2,v2 = h2 
    # find a,b st p1+a*v1 = p2+b*v2 
    # a*v1 - b*v2 = p2-p1

    a = sympy.var("a")
    b = sympy.var("b")

    es = a*v1 + p1 - (b*v2 + p2)
    eqs = [sympy.Eq(e,0) for e in es]
    sol = sympy.solve(eqs)

    printx(h1,h2,sol)
    if sol and sol[a]>=0 and sol[b]>=0:
        pt = sol[a]*v1 + p1 

        return pt 
    return None

test_area = Interval(7,27) if is_ex else Interval(200000000000000,400000000000000)

# tot = 0
# i = 0
# for p1,p2 in itertools.combinations(hails_xy,r=2):
#     c = collide(p1,p2)
#     if c and all(p in test_area for p in c):
#         tot += 1
#     i += 1
#     if i % 1000 == 0:
#         print(i,tot)

# print("Part 1:", tot)

eqs = []
rp = Vector([sympy.Symbol(f"rp{i}") for i in range(3)])
rv = Vector([sympy.Symbol(f"rv{i}") for i in range(3)])

for i,(hp,hv) in enumerate(hails_xyz[:3]):
    t = sympy.Symbol(f"t{i}")

    es = rp + t*rv - (hp+t*hv)
    for e in es.data:
        eqs.append(sympy.Eq(e,0))

print(eqs)
sol = sympy.solve(eqs)
print(sol)

rps = [sol[0][v] for v in rp]
print("Part 2:", sum(rps))

# TODO: make a non-sympy solution