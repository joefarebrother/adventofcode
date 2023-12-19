from utils import *

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
        res = IntervalSet()

        for dest_start, src_start, rng_len in self.lines:
            cut = Interval(src_start,len=rng_len)

            res |= (remaining & cut).shift(dest_start-src_start)
            remaining -= cut 

        res |= remaining
        return res

    
gs = inp_groups()
seeds = ints_in(gs[0][0])

grps = mapl(Group, gs[1:])

for g in grps:
    #print(seeds)
    seeds = [g.translate(s) for s in seeds]

print("Part 1:", min(seeds))

seeds1 = ints_in(gs[0][0])

seed_ranges = IntervalSet([Interval(a,len=b) for a,b in chunks(seeds1, 2)])

for g in grps:
    seed_ranges = g.translate_ranges(seed_ranges)
    #print(len(seed_ranges))
    # if len(seed_ranges) > 100000:
    #     raise Exception()
    
print("Part 2:", seed_ranges.intervals[0].start)
