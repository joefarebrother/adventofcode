from utils import *
import sympy
import operator as ops

eqs = {}
for line in inp_readlines():
    v, ex = line.split(": ")
    eqs[v] = ex


def calc(var, scope):
    if var in scope:
        return scope[var]
    ex = eqs[var]
    try:
        res = int(ex)
        scope[var] = res
        return res
    except ValueError:
        pass
    l, op, r = ex.split()
    res = {"+": ops.add, "-": ops.sub, "*": ops.mul, "/": ops.truediv}[op](calc(l, scope), calc(r, scope))
    scope[var] = res
    return res


print("Part 1:", calc("root", {}))

eqs["root"] = re.sub(r'[+\-*/]', "-", eqs["root"])

eq = calc("root", {"humn": sympy.Symbol("x")})

print(eq)
print("Part 2:", int(sympy.solve(eq)[0]))
