from utils import *
import json

class Rule:
    def __init__(self, line):
        rl,self.dest = line.split(":")
        if "<" in rl:
            self.sym = "<"
            self.axis,n = rl.split("<")
            self.val = int(n)
        elif ">" in rl:
            self.sym = ">"
            self.axis,n = rl.split(">")
            self.val = int(n)
        else:
            raise Exception("bad rule")
        
    def matches(self, part):
        if self.sym == "<":
            return part.p[self.axis] < self.val 
        else:
            return part.p[self.axis] > self.val 
        
    def __str__(self):
        return f"{self.axis} {self.sym} {self.val} : {self.dest}"

class Workflow:
    def __init__(self, line):
        self.name,rest = line.split("{")
        rest = rest[:-1]
        rules = rest.split(",")
        self.rules, self.default = mapl(Rule,rules[:-1]), rules[-1]
        #printx(line, self.rules)

    def process(self,part):
        for r in self.rules:
            if r.matches(part):
                return r.dest
        return self.default
    
class Part:
    def __init__(self, line):
        #printx(line)
        self.p = json.loads(re.sub(r'([xmas])=(\d+)', r'"\1":\2', line))

    def score(self):
        return sum(self.p.values())

workflows_, parts = inp_groups()
workflows = {}

for w in workflows_:
    wk = Workflow(w)
    workflows[wk.name] = wk

tot = 0
for p in parts:
    p = Part(p)
    wf = workflows["in"]
    while True:
        nwf = wf.process(p)
        if nwf == "R":
            break
        if nwf== "A":
            tot += p.score()
            break 
        wf = workflows[nwf]

print("Part 1:", tot)

class PartInterval:
    def __init__(self, dims=None):
        if dims is None:
            self.dims = [(1,4000)]*4
        else:
            self.dims = dims

    @classmethod
    def axis_idx(cls,axis):
        return "xmas".find(axis)

    def split(self, axis, val, sym):
        iv = self.dims[PartInterval.axis_idx(axis)]
        cut = (1,val-1) if sym == "<" else (val+1,4000)
        cut2 = (val,4000) if sym == "<" else (1,val)

        l = intersect_irange(iv,cut)
        r = intersect_irange(iv,cut2)

        if l is not None:
            li = PartInterval(self.dims.copy())
            li.dims[PartInterval.axis_idx(axis)] = l
            l = li 
        if r is not None:
            ri = PartInterval(self.dims.copy())
            ri.dims[PartInterval.axis_idx(axis)] = r
            r = ri 

        return l,r 
    
    def __repr__(self):
        return f"PartInterval({self.dims})"

    def intersect(self, other):
        res = []
        for s, o in zip(self.dims, other.dims, strict=True):
            rint = intersect_irange(s,o)
            if rint:
                res.append(rint)
            else:
                return None
        return PartInterval(res)
    
    def difference(self, other):
        res = []
        if not self.intersect(other):
            return [self]

        locur = [d[0] for d in self.dims]
        hicur = [d[1] for d in self.dims]

        for d, (c0, c1, (o0, o1)) in enumerate(zip(locur, hicur, other.dims, strict=True)):
            #       oooooooooooooo              oooooooooooooo
            #       o            o              o            o
            #  ccccccccccc       o         rrrrrcccccc       o
            #  c    o    c       o         r   rc    c       o
            #  c    o    c       o         r   rc    c       o
            #  c    ooooocoooooooo    =>   r   rcoooocoooooooo
            #  c         c                 r   rc    c
            #  c         c                 r   rc    c
            #  c         c                 r   rc    c
            #  c         c                 r   rc    c
            #  c         c                 r   rc    c
            #  ccccccccccc                 rrrrrcccccc
            #

            # left
            if c0 < o0 <= c1:
                res.append((tuple(locur), modify_idx(tuple(hicur), d, o0-1)))
                locur[d] = o0
            # right
            if c0 <= o1 < c1:
                res.append((modify_idx(tuple(locur), d, o1+1), tuple(hicur)))
                hicur[d] = o1

        res2 = []
        for (rlo, rhi) in res:
            res2.append(PartInterval(zip(rlo,rhi)))

        return res2
    
    def volume(self):
        return math.prod(c1-c0+1 for c0, c1 in self.dims)
    
class PartSet:
    def __init__(self, parts):
        self.parts = parts 
        # self.assert_consistent()

    def __repr__(self):
        return f"PartSet({self.parts})"

    def union(self, other):
        res = self.parts.copy()
        for o in other.parts:
            op = [o]
            for s in self.parts:
                nop = []
                for no in op:
                    nop += no.difference(s)
                op = nop 
            res += op 
        return PartSet(res)
    
    __or__ = union

    def split(self, axis, val, sym):
        ls = []
        rs = []
        for p in self.parts:
            l,r = p.split(axis, val, sym)
            if l:
                ls.append(l)
            if r:
                rs.append(r)
        return PartSet(ls), PartSet(rs)

    def volume(self):
        return sum(p.volume() for p in self.parts)
    
    def assert_consistent(self):
        for p1,p2 in it.combinations(self.parts,2):
            assert p1.intersect(p2) is None, (p1,p2,p1.intersect(p2))
    
wfg = FGraph(adj=lambda wf:[] if wf in "AR" else [r.dest for r in workflows[wf].rules]+[workflows[wf].default])
topsort = wfg.topsort("in")

wfparts = defaultdict(lambda:PartSet([]))
wfparts["in"] = PartSet([PartInterval()])

for wf in topsort:
    # print(wf)
    parts = wfparts[wf]
    if wf in "AR":
        continue
    wf = workflows[wf]

    for r in wf.rules:
        # print(wf.name, r, parts)
        ls,rs = parts.split(r.axis, r.val, r.sym)
        assert (ls.volume() + rs.volume() == parts.volume()), (parts, ls, rs)
        wfparts[r.dest] |= ls 
        parts = rs 

    wfparts[wf.default] |= parts 

print("Part 2:", wfparts["A"].volume())

assert(wfparts["A"].volume()+wfparts["R"].volume() == PartInterval().volume())

