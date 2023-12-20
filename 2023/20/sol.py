from utils import *


class Module:
    def __init__(self, line):
        n, ds = line.split(" -> ")
        if n in ["broadcaster", "output"]:
            self.kind="b"
            self.name = n 
        else:
            self.kind = n[0]
            self.name = n[1:]
        self.destt = mapl(lambda x: x.strip(), ds.split(",")) if ds else []
        self.dest = []
        self.inp = []
        self.inpstate = []
        self.flipstate = False

        self.dep = set()
        self.cache = {}
        self.period = None
        self.pstart = None
        self.results = []
        self.cur_pulses = []

    def rcv(self, src, pulse):
        if self.kind == "%":
            if pulse:
                return None 
            else:
                self.flipstate ^= True 
                return self.flipstate 
        if self.kind == "&":
            #printx(self.inp)
            src_idx = [m.name for m in self.inp].index(src)
            self.inpstate[src_idx] = pulse 
            return not all(self.inpstate)
        if self.kind == "b":
            return False
        return None
    
    def __repr__(self):
        return f"<{self.name}>"
    
    def state(self):
        return self.flipstate,tuple(self.inpstate)
    
    def dep_state(self):
        return tuple(mods[m].state() for m in self.dep)
    
    def rcv_cache(self, src, pulse):
        res = self.rcv(src,pulse)
        self.cur_pulses.append(res)
        return res
    
    def reset(self, btnidx):
        st = self.dep_state()

        if st in self.cache and not self.period:
            nbtnidx,pls = self.cache[st]
            self.pstart = nbtnidx 
            self.period = btnidx - nbtnidx 
            print("Cache hit", self.name, self.period, self.pstart, set(m for m in mods if mods[m].period is None))

        if self.period is not None:
            expect = ((btnidx-self.pstart)%self.period+self.pstart, self.cur_pulses)
            assert self.cache[st] == expect, (self.name,self.cache[st],expect)
        else:
            #print(self.name, btnidx, self.cur_pulses)
            self.cache[st] = (btnidx,self.cur_pulses)
        self.results.append(self.cur_pulses)
        self.cur_pulses = []


mods = mapl(Module, inp_readlines())
mods = {m.name:m for m in mods}
for m in list(mods.values()):
    for d in m.destt:
        if d not in mods:
            mods[d] = Module(f"b{d} -> ")
        m.dest.append(mods[d])
        mods[d].inp.append(m)
        mods[d].inpstate.append(False)


def press(btnidx):

    q = deque([("broadcaster", None, False)])
    los = 0
    his = 0
    while q:
        dest,src,pulse = q.popleft()
        if pulse:
            his += 1
        else:
            los += 1
            if dest == "rx":
                return his,los,True
        
        printx(f"{src} --{pulse}--> {dest}")
        nxt = mods[dest].rcv_cache(src,pulse)
        if nxt is not None:
            for d in mods[dest].destt:
                q.append((d,dest,nxt))


    for m in mods.values():
        m.reset(btnidx)
            
    return his,los,False

def press_many(n):
    los = 0
    his = 0

    for i in range(n):
        nhis,nlos,rx = press(i)
        if rx:
            return los,his,i
        los+=nlos
        his += nhis 

        if len([m for m in mods.values() if m.period is not None]) == len(mods)-2:
            return los,his,los*his

    return los,his,los*his 

# print("Part 1:",press_many(1000))

gr = FGraph(lambda x: mods[x].destt)
igr = FGraph(lambda x: [m.name for m in mods[x].inp])
for g in gr.topsort("broadcaster"):
    g = mods[g]
    inps = ", ".join([i.kind+i.name for i in g.inp])
    outs = ", ".join([i.kind+i.name for i in g.dest])

    print(f"{inps:>30} -> {g.kind}{g.name} -> {outs}")

for m in mods:
    mods[m].dep = set(n for n,_ in igr.DFS(m))
    
press_many(10000000)

for inp in mods["rm"].inp:
    print(inp, inp.period, inp.results[0])

print("Part 2:", math.lcm(*[m.period for m in mods["rm"].inp]))