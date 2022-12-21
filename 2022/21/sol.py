from utils import *
import sympy

eqs = {}
for line in inp_readlines():
    v, ex = line.split(": ")
    m = re.findall(r'(....) . (....)', ex)
    deps = []
    if m:
        deps = list(m[0])
    eqs[v] = (ex, deps)

print(eqs)

scope = {}
for v in FGraph(adj=lambda v: eqs[v][1]).topsort("root")[::-1]:
    scope[v] = eval(eqs[v][0], scope)

print("Part 1:", int(scope["root"]))

eqs["humn"] = ('sympy.Symbol("x")', [])
eqs["root"] = (re.sub(r'[+\-*/]', "-", eqs["root"][0]), eqs["root"][1])

scope = {"sympy": sympy}
for v in FGraph(adj=lambda v: eqs[v][1]).topsort("root")[::-1]:
    scope[v] = eval(eqs[v][0], scope)

print(scope["root"])
print("Part 2:", ints(sympy.solve(scope["root"])))
