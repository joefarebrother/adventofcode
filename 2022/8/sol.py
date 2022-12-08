from utils import *

inp = Grid(0, ints=True)


def vis(p):
    for d in neighbours(0):
        p0 = p
        while p0 in inp and p0+d in inp:
            if inp[p0+d] >= inp[p]:
                break
            p0 += d
        else:
            return True
    return False


print(sum(vis(p) for p in inp))


def score(p, d):
    p0 = p
    i = 1
    while p0 in inp and p0+d in inp:
        if inp[p0+d] >= inp[p]:
            return i
        p0 += d
        i += 1
    return i-1


def tscore(p):
    return math.prod(score(p, d) for d in neighbours(0))


print(max(tscore(p) for p in inp))
