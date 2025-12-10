from utils import *
import sympy

class Machine:
    lights: list 
    buttons: list 
    joltage: list 

    def __init__(self,row):
        printx(row)
        l, b, j = match(r"\[([\.#]*)\] (.*) (\{.*\})", row)
        self.lights = [c=='#' for c in l]
        self.buttons = [ints_in(sec) for sec in b.split("(")[1:]]
        self.joltage = ints_in(j)

    def presses(self):
        lbits = 0
        for i,c in enumerate(self.lights):
            if c:
                lbits |= 1 << i 
        bbits = []
        for bs in self.buttons:
            bbits.append(reduce(lambda a,b: a|b, [1<<b for b in bs], 0))

        valid = []
        for comb in it.product([True,False], repeat=len(bbits)):
            res = reduce(lambda a,b:a^b, [b for b,c in zip(bbits,comb) if c], 0)
            if res == lbits:
                valid.append(comb)

        return min(map(sum, valid))

    def press_jolt(self):
        vars = sympy.symbols(f"x:{len(self.buttons)}")
        eqs = []
        for i, j in enumerate(self.joltage):
            eq = sum(vars[b] for b,bx in enumerate(self.buttons) if i in bx) 
            eqs.append(sympy.Eq(eq,j))

        size, maxs, sol, deps = self.find_good_search_space(vars, eqs)

        return self.search(deps, maxs, sol)

    def prune_search_space(self,sol,deps):
        max_jolts = max(self.joltage)
        maxs = {v:max_jolts for v in deps}
        changed=True 
        while changed:
            changed=False
            for s in sol.values():
                sub = {}
                for v in deps:
                    if s.coeff(v) > 0:
                        sub[v] = maxs[v]
                    else:
                        sub[v] = 0 
                mx = s.subs(sub)
                for v in deps:
                    if s.coeff(v) < 0:
                        nmx = int(mx/-s.coeff(v))
                        if nmx < maxs[v]:
                            maxs[v] = nmx 
                            changed=True
        return maxs
    
    def find_good_search_space(self, vars, eqs):
        sol = sympy.solve(eqs)
        print("sol",sol)

        deps = [v for v in vars if v not in sol]

        maxs = self.prune_search_space(sol, deps)
        size = math.prod(m+1 for m in maxs.values())

        print("maxs", maxs, "size", size)

        if size < 10000:
            return size, maxs, sol, deps 

        
        best = size, maxs, sol, deps
        lsol = len(sol)

        import random
        for _ in range(10):
            print("retrying")
            vars = list(vars)
            random.shuffle(vars)
            alt_vars = vars[:lsol]
            
            sol = sympy.solve(eqs, alt_vars, dict=True)
            if len(sol) != 1:
                print("bad len", alt_vars, sol, len(sol))
                continue
            sol = sol[0]

            deps = [v for v in vars if v not in sol]
            print(sol, deps)

            maxs = self.prune_search_space(sol, deps)
            size = math.prod(m+1 for m in maxs.values())

            print("maxs", maxs, "size", size)
            if size < 10000:
                return size, maxs, sol, deps 
            if size < best[0]:
                best = size, maxs, sol, deps 

        return best

    def search(self, deps, maxs, sol):
        size = math.prod(m+1 for m in maxs.values())
        print("searching")
        best = math.inf
        b_sol = None
        prog = 0
        for comb in it.product(*[range(maxs[v]+1) for v in deps]):
            repl = dict(zip(deps,comb))
            sub = [r.subs(repl) for r in sol.values()]
            if all(s >= 0 and s == int(s) for s in sub):
                best = min(best, sum(sub)+sum(comb))
                b_sol = (repl, sub)
            prog += 1 
            if prog % 10000 == 0:
                print(f"{prog}/{size}")
        print(b_sol)
        return best
            
    
ms = mapl(Machine, inp_readlines())

#print("Part 1:", sum(m.presses() for m in ms))

print("Part 2:", sum(m.press_jolt() for m in ms))