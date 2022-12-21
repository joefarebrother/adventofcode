from utils import *
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


print("Part 1:", int(calc("root", {})))


@dataclass
class Term:
    """a*x + b"""
    a: int
    b: int

    def __str__(self):
        return f"{self.a}*x + {self.b}"

    def __add__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Term(self.a, self.b+other)
        if isinstance(other, Term):
            a = self.a+other.a
            b = self.b+other.b
            if a == 0:
                return b
            return Term(a, b)
        return NotImplemented

    __radd__ = __add__

    def __neg__(self):
        return Term(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return other + (-self)

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            if other == 0:
                return 0
            return Term(self.a*other, self.b*other)
        return NotImplemented

    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Term(self.a/other, self.b/other)

    def solve(self):
        return -self.b/self.a


eqs["root"] = re.sub(r'[+\-*/]', "-", eqs["root"])

t = calc("root", {"humn": Term(1, 0)})
print(t)

print("Part 2:", int(t.solve()))
