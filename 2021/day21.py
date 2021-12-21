from utils import *

inp = readlines(21)

die = 0


def roll():
    global die
    die += 1
    return mod_inc(die, 100)


def mod_inc(a, b):
    return ((a-1) % b)+1


ps = [ints_in(l)[1] for l in inp]
scores = [0, 0]

p = 1
while all(s < 1000 for s in scores):
    p = 1-p
    ps[p] = mod_inc(ps[p] + roll()+roll()+roll(), 10)
    scores[p] += ps[p]

print("Part 1:", scores, die, min(scores)*die)

univ = Counter()  # key = ((p1pos,p2pos),(p1sc,p2sc))
ps = [ints_in(l)[1] for l in inp]
univ[tuple(ps), (0, 0)] = 1
wins = [0, 0]

p = 1
while univ:
    p = 1-p
    nuniv = Counter()
    for (ps, sc), u in univ.items():
        for ds in it.product(irange(3), repeat=3):
            roll = sum(ds)
            np = mod_inc(ps[p]+roll, 10)
            nsc = sc[p]+np
            nps = modify_idx(ps, p, np)
            nscs = modify_idx(sc, p, nsc)
            if nsc >= 21:
                wins[p] += u
            else:
                nuniv[(nps, nscs)] += u
    univ = nuniv

print("Part 2:", wins, max(wins))
