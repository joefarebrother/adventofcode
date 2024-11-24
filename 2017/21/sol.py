from utils import *

start = Grid(""".#.
..#
###
""".split("\n"))

start.draw()
print(dict(start.items()))

@dataclass
class D8:
    # <xa | x2 = a4 = e, xa = a-1x>
    rot: complex
    flip: bool

    def __mul__(self, other):
        if isinstance(other, D8): 
            return D8(self.rot * (1/other.rot if self.flip else other.rot), self.flip ^ other.flip)
        return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, complex) or isinstance(other, IVec2):
            c = other*self.rot
            return c.conjugate() if self.flip else c
        return NotImplemented

    def inv(self):
        if self.flip:
            return self
        else:
            return D8(1/self.rot, False)

    def __str__(self):
        i = [1j**i for i in range(4)].index(self.rot)
        if not i:
            return "f" if self.flip else "e"
        else:
            rs = "r" if i == 1 else f"r{i}"
            return f"{rs} * f" if self.flip else rs


r = D8(1j, False)
f = D8(1, True)
e = D8(1, False)
assert (r*r*r*r == e)
assert (f*f == e)
assert (f*r*f == r.inv())
d8 = [D8(rot, flip)
      for (rot, flip) in it.product(neighbours(0), [False, True])]
r2 = r*r
r3 = r.inv()

rules = {}
for r in inp_readlines():
    r,v = r.split(" => ")
    rules[r]=v

def step(g: Grid):
    if g.height % 2 == 0:
        # print("=== EVEN ===")
        res = Grid()
        for x in range(0,g.width,2):
            for y in range(0,g.width,2):
                sub = Grid()
                for dp in Rectangle((0,0),(1,1)) :
                    sub[dp] = g[(x,y)+dp]
                assert len(sub) == 4
                enhance(res,sub, ((x//2*3),(y//2*3))) 
    else:
        # print("=== ODD ===")
        res = Grid()
        for x in range(0,g.width,3):
            for y in range(0,g.width,3):
                sub = Grid()
                for dp in Rectangle((0,0),(2,2)) :
                    sub[dp] = g[(x,y)+dp]
                    assert sub[dp] != None, (x,y, g.width, ((x,y)+dp), sorted(g.items()))
                    # print(dp, (x,y)+dp, g[(x,y)+dp])
                    # sub.draw()
                assert len(sub) == 9, sub
                enhance(res,sub, ((x//3*4),(y//3*4))) 

    assert None not in list(res.values()) 
    return res

def get_in_ori(tile, ori, pos, size):
    cent = (size-1)*(0.5+0.5j)
    #tile.draw()
    
    #print(ori, pos, size, cent, (complex(pos)-cent)*ori.inv()+cent, tile[(complex(pos)-cent)*ori.inv()+cent])
    return tile[(complex(pos)-cent)*ori.inv()+cent]

def flip(sub, ori):
    #sub.draw()
    # print(ori)
    res = ""
    for dp in sub.bounding_box:
        if dp.x == 0:
            res += "/"
        res += get_in_ori(sub, ori, dp, sub.width)
        
    #print(res)
    return res[1:]

test = False
def enhance(res, sub, p):
    global test
    # sub.draw()
    #print(p, res.width, sub.width)
    #print(sorted(sub.items()))
    for ori in d8:
        if (r:=flip(sub, ori)) in rules:
            if test:
                print(r, rules[r], p)
                test = False
            #print("found ori", ori)
            new = rules[r]
            newg = Grid(new.split("/"))
            for dp in newg.bounding_box:
                res[p+dp] = newg[dp]
            #print("enhanced", ori)
            return
    assert False

g = start
for i in range(5):
    g = step(g)
    print("=== step", i, sorted(g.items()))
    
    g.draw()
assert(str(g.values()).count("#") == 208, str(g.values()).count("#"))

start1 = {flip(start, e): 1}

def step_smart(g):
    res = Counter()
    for (sub, amt) in g.items():
        gr = Grid(sub.split("/"))
        ngr = step(gr)
        if ngr.width < 9:
            res[flip(ngr,e)] += amt 
        else:
            assert ngr.width == 9
            for p in Rectangle((0,0),(2,2)):
                sub = Grid()
                p = 3*p
                for dp in Rectangle((0,0),(2,2)):
                    sub[dp]=ngr[p+dp]
                #print(sorted(sub.items()))
                res[flip(sub,e)] += amt
    return res


test = False

g = start1
for i in range(18):
    print(g)
    g = step_smart(g)
    if (i == 4):
        print([(amt, s, s.count("#")) for (s,amt) in g.items()])
        assert (x := sum(amt*s.count("#") for (s,amt) in g.items())) == 208, x


t = 0
for s,amt in g.items():
    t += amt*s.count("#")

print("Part 2:", t)