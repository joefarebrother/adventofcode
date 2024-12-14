import sympy.solvers
from utils import *
import sympy

@dataclass
class Claw:
    a: P 
    b: P 
    prize: P

    def __init__(self, lines):
        self.a = (P(*ints_in(lines[0]))) # when using the part 1 solver, using complex numbers rather than P (my point class) has a significant performance boost
        self.b = (P(*ints_in(lines[1]))) # current version uses only the part 2 solver for which P is slightly faster
        self.prize = (P(*ints_in(lines[2])))

    def win(self):
        # part 1 solver; now unused bc the part 2 solver is much faster and subsumes it
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

        # # original solution 
        # s = sympy.solve(eqs)
        # na, nb = s[na], s[nb]

        # faster solution (use function specifically for linear equations)
        s = sympy.solvers.linsolve(eqs, na, nb)
        na, nb = only(s)

        #if na.round() == na.round(3) and nb.round() == nb.round(3): # when using complex, results are returned as floats that we need to be careful about handling imprecision with round
        if na.denominator == 1 and nb.denominator == 1: # when using point class P, all equations passed to sympy are integers thus results are returned as rational numbers
            return (na*3+nb) 
        else:
            return 0 
        
        # cases that i didn't handle that didn't actually show up in the input and likely wouldn't show up in anyone's input:
        # - the solutions including negative numbers (e.g. na3, nb=-1)
        # - there being multiple solutions sue to the buttons being "linearly dependant", i.e. there's a constant you can multiply A by to get B
        # - - in this case, finding the solution with the minimum cost would be more challenging
    
# mapl is my own utility that's simply a wrapper around map that converts the result to a list 
# this is relevant bc map returns a generator, and after iterating over it once it's exhausted and further attempts to iterate it give no result
# inp_groups is a utility that splits the input into groups by double-newlines, and splits each group into a list of lines
claws = mapl(Claw, inp_groups()) 

print("Part 1:", sum([c.win2() for c in claws]))

for c in claws:
    # assert c.win() == c.win2(), (c, c.win(), c.win2())
    c.adjust()

print("Part 2:", sum([c.win2() for c in claws]))

# performace comparisons

# solve

# real    0m20.358s
# user    0m20.264s
# sys     0m0.060s

# linsolve

# real    0m3.211s
# user    0m3.142s
# sys     0m0.062s

# linsolve with point class instead of complex

# real    0m37.986s
# user    0m37.692s
# sys     0m0.097s

# most of that time taken is in the part 1 solver. removing the assert statement to verify that both solvers give the same result gives:

# real    0m18.073s
# user    0m17.992s
# sys     0m0.043s

# removing the part 1 solver altogether:

# point class

# real    0m0.931s
# user    0m0.884s
# sys     0m0.043s

# complexes

# real    0m1.403s
# user    0m1.352s
# sys     0m0.047s 

# is in fact slightly worse. probably due to floating point handling.

# point class, no p1, solve instead on linsolve
# real    0m1.777s
# user    0m1.715s
# sys     0m0.056s

# current and fastest complete version: point class, linsolve, part 1 is nt skipped as in abvoe tests but uses the part 2 solver
# real    0m1.400s
# user    0m1.320s
# sys     0m0.063s