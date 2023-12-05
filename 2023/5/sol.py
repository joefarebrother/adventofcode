from utils import *

def cut_range(rng, cut):
    mid = intersect_irange(rng, cut)
    if not mid:
        return rng, None, (0,0)

    l1, h1 = rng 
    l2, h2 = mid
    if l1 < l2:
        r1 = (l1, l2)
    else:
        r1 = (0,0)
    if h2 > h1:
        r2 = (h1,h2)
    else:
        r2 = (0,0)
    

    return r1, mid, r2


class Group:
    def __init__(self, gr):
        self.name = gr[0]
        self.lines = mapl(ints_in,gr[1:])

    def translate(self,n):
        for dest_start, src_start, rng_len in self.lines:
            if n in range(src_start,src_start+rng_len):
                return n-src_start+dest_start
        return n
    
    def translate_ranges(self, rs):
        remaining = rs
        res = []

        for dest_start, src_start, rng_len in self.lines:
            cut = (src_start, src_start+rng_len)
            if is_ex:
                print(self.name, remaining, cut)

            new_remaining = []
            for rn in remaining:
                lo, mid, hi = cut_range(rn, cut)
                new_remaining += [lo,hi]
                if mid:
                    res.append((dest_start-src_start+mid[0], dest_start-src_start+mid[1]))
            remaining = list(filter(lambda lh: lh[1]>lh[0], new_remaining))



        res += remaining
        return res

    
gs = inp_groups()
seeds = ints_in(gs[0][0])

grps = mapl(Group, gs[1:])

for g in grps:
    print(seeds)
    seeds = [g.translate(s) for s in seeds]

print("Part 1:", min(seeds))

seeds1 = ints_in(gs[0][0])

seed_ranges = [(a, a+b) for a,b in chunks(seeds1, 2)]

for g in grps:
    seed_ranges = g.translate_ranges(seed_ranges)
    print(len(seed_ranges))
    if len(seed_ranges) > 100000:
        raise Exception()
    
print("Part 2:", min(r[0] for r in seed_ranges))
