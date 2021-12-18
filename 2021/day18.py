from utils import *

oginp = readlines(18)
inp = [eval(i) for i in oginp]


def add_adjacent(n, pars, idx):
    opp = 1-idx
    for (p, i) in reversed(pars):
        if i == opp:
            if type(p[idx]) == int:
                p[idx] += n[idx]
            else:
                p = p[idx]
                while type(p[opp]) != int:
                    p = p[opp]
                p[opp] += n[idx]
            return


def check_explodes(n, pars=None):
    if pars == None:
        pars = []
    if type(n) == int:
        return False
    if len(pars) < 4:
        return check_explodes(n[0], pars+[(n, 0)]) or check_explodes(n[1], pars+[(n, 1)])
    add_adjacent(n, pars, 0)
    add_adjacent(n, pars, 1)
    p, i = pars[-1]
    p[i] = 0
    return True


def check_splits(n, pars=None):
    if pars == None:
        pars = []
    if type(n) == int:
        if n < 10:
            return False
        p, i = pars[-1]
        p[i] = [math.floor(n/2), math.ceil(n/2)]
        return True
    return check_splits(n[0], pars+[(n, 0)]) or check_splits(n[1], pars+[(n, 1)])


def mag(n):
    if type(n) == int:
        return n
    return 3*mag(n[0]) + 2*mag(n[1])


def reduce(n):
    while check_explodes(n) or check_splits(n):
        pass
    return n


def add(n, m):
    return reduce([n, m])


n = inp[0]
for m in inp[1:]:
    n = add(n, m)

print("Part 1:", mag(n))

maxm = 0
for i, j in it.permutations(oginp, 2):
    m = mag(add(eval(i), eval(j)))
    maxm = max(maxm, m)

print("Part 2:", maxm)
