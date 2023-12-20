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

box = CuboidSet(Cuboid([(1,4000)]*4))

def cut(cubs, axis, val, sym):
    cub = hyperplane("xmas".find(axis),4,val,sym)
    return cubs & cub, cubs-cub
    
wfg = FGraph(adj=lambda wf:[] if wf in "AR" else [r.dest for r in workflows[wf].rules]+[workflows[wf].default])
topsort = wfg.topsort("in")

wfparts = defaultdict(CuboidSet)
wfparts["in"] = box

for wf in topsort:
    # print(wf)
    parts = wfparts[wf]
    if wf in "AR":
        continue
    wf = workflows[wf]

    for r in wf.rules:
        # print(wf.name, r, parts)
        ls,rs = cut(parts, r.axis, r.val, r.sym)
        assert (ls.volume() + rs.volume() == parts.volume()), (parts, ls, rs)
        wfparts[r.dest] |= ls 
        parts = rs 

    wfparts[wf.default] |= parts 

print("Part 2:", wfparts["A"].volume())

assert(wfparts["A"].volume()+wfparts["R"].volume() == box.volume())

