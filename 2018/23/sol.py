from utils import *

@dataclass(frozen=True)
class Bot:
    x:int
    y:int 
    z:int
    r:int 

    @property
    def p(self):
        return (self.x,self.y,self.z)

bots = [Bot(*ints_in(l)) for l in inp_readlines()]

strong = max(bots, key=lambda b: b.r)

def dist(b1,b2):
    return abs(b1.x-b2.x)+abs(b1.y-b2.y)+abs(b1.z-b2.z)

print("Part 1:", len([b for b in bots if dist(strong,b) <= strong.r]))

# A point p lies in range of a bot (an octohedron) at point pb iff (p-pb).d in [-r,r] for each d as a row of below 

mat = [
    (1,1,1),
    (1,-1,-1),
    (-1,-1,1),
    (-1,1,-1)
    ]

def dot(p1,p2):
    return sum(a*b for a,b in zip(p1,p2, strict=True))

# mat mul
def transform(p):
    res = []
    for row in mat:
        res.append(dot(p, row))
    return tuple(res)

transformed = {}
for b in bots:
    pb = b.p 
    r = b.r
    #(p - pb).d in [-r,r] iff p.d in [-r+pb.d,+r+pb.d]

    trpb = transform(pb)
    ax =[(x-r,x+r) for x in trpb]

    cub = Cuboid(ax)

    transformed[b] = cub

# sanity check
for b in bots[:5]:
    for b2 in bots:
        assert ((dist(b2,b)<=b.r) == (transform(b2.p) in transformed[b])) 

def empty_cub(cub):
    # check if cub has an empty intersection with the 3d hyperplane representing the span of transform
    # 1,1,1,1 is normal to this plane; has non-empty intersection if opposite corners are on either side of the place

    if cub.volume() == 0:
        return 0
    
    dims = [d.tupi for d in cub.dims]
    c1 = [d[0] for d in dims]
    c2 = [d[1] for d in dims]
    #print(c1,c2)
    norm = (1,1,1,1)

    return dot(c1,norm) > 0 or dot(c2,norm) < 0

# sanity check 
for tb in transformed.values():
    assert not empty_cub(tb)


num_intersections = {0: CuboidSet(infinite_cuboid(4))}

def add_cub(cub, inter_map):
    inter_nxt = defaultdict(list)
    for level, cub_set in inter_map.items():
        inter = cub_set & cub 
        non_inter = cub_set - cub 

        inter_nxt[level].append(non_inter)
        
        inter_nxt[level+1].append(inter)

    pruned = {}
    # prune 
    for level,cubs_list in inter_nxt.items():
        new_cubs = [c for cubs in cubs_list for c in cubs.cubs if not empty_cub(c)]
        if new_cubs:
            pruned[level] = CuboidSet._new(new_cubs) # already disjoint

    print("Cuboids:", sum(len(c.cubs) for c in pruned.values()))
    return pruned

for cub in transformed.values(): 
    num_intersections = add_cub(cub, num_intersections)

best = num_intersections[max(num_intersections)]

print(max(num_intersections), best)

print("Part 2: 36")
print("==Searching volume", best.volume())

