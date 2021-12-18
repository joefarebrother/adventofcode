from utils import *

oginp = readlines(18)
inp = [eval(i) for i in oginp]


def check_explodes(n, pars=None):
    if pars == None:
        pars = []
    if type(n) == int:
        return False
    if len(pars) < 4:
        return check_explodes(n[0], pars+[(n, 0)]) or check_explodes(n[1], pars+[(n, 1)])
    # find left
    #printx("Exploding:", n)
    for (p, i) in reversed(pars):
        if i == 1:  # first ancestor for which this is the right child of
            if type(p[0]) == int:
                p[0] += n[0]
                break
            else:
                p = p[0]
                while type(p[1]) != int:
                    p = p[1]
                p[1] += n[0]
            break
    # find right
    for (p, i) in reversed(pars):
        if i == 0:  # first ancestor for which this is the left child of
            if type(p[1]) == int:
                p[1] += n[1]
                break
            else:
                p = p[1]
                while type(p[0]) != int:
                    p = p[0]
                p[0] += n[1]
                break
    p, i = pars[-1]
    p[i] = 0
    return True


def check_splits(n, pars=None):
    #printx("Checking splits:", n)
    if pars == None:
        pars = []
    if type(n) == int:
        if n < 10:
            return False
        #printx("Splitting:", n)
        p, i = pars[-1]
        p[i] = [math.floor(n/2), math.ceil(n/2)]
        return True
    return check_splits(n[0], pars+[(n, 0)]) or check_splits(n[1], pars+[(n, 1)])


def mag(n):
    if type(n) == int:
        return n
    return 3*mag(n[0]) + 2*mag(n[1])


def reduce(n):
    printx("Reducing:", n)
    while check_explodes(n) or check_splits(n):
        pass
    printx("Done reducing:", n)
    return n


def add(n, m):
    return reduce([n, m])


n = inp[0]
for m in inp[1:]:
    n = add(n, m)

print("Part 1:", mag(n))

maxm = 0
for i, j in itertools.product(oginp, repeat=2):
    m = mag(add(eval(i), eval(j)))
    maxm = max(maxm, m)

print("Part 2", maxm)
