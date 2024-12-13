from utils import *
import sympy

@dataclass
class Claw:
    a: P 
    b: P 
    prize: P

    def __init__(self, lines):
        self.a = complex(P(*ints_in(lines[0])))
        self.b = complex(P(*ints_in(lines[1])))
        self.prize = complex(P(*ints_in(lines[2])))

    def win(self):
        best = math.inf 
        for na in range(101):
            for nb in range(101):
                if na*self.a + nb*self.b == self.prize:
                    cost = 3*na + nb
                    best = min(best, cost)
        printx(self, best)
        if best < math.inf:
            return best 
        return 0
    
    def adjust(self):
        self.prize += 10000000000000+10000000000000j

    def win2(self):
        na = sympy.Symbol("na")
        nb = sympy.Symbol("nb")

        eqs = [self.a.real * na + self.b.real * nb - self.prize.real, self.a.imag * na + self.b.imag * nb - self.prize.imag]
        s = sympy.solve(eqs)

        na, nb = s[na], s[nb]

        if na == int(na) and nb == int(nb):
            return int(na*3+nb) 
        else:
            return 0 
    
claws = mapl(Claw, inp_groups())

print(sum([c.win() for c in claws]))

for c in claws:
    assert c.win() == c.win2()
    c.adjust()

print(sum([c.win2() for c in claws]))
