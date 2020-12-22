# pylint: disable=unused-wildcard-import
from utils import *

p1, p2 = groups("22.in")
p1 = ints(p1.split("\n")[1:])
p2 = ints(p2.split("\n")[1:])

while p1 and p2:
    c1, c2 = p1.pop(0), p2.pop(0)
    if c1 > c2:
        w = p1
    else:
        w = p2
    w.append(max(c1, c2))
    w.append(min(c1, c2))

print(w)


def score(w):
    w = w[::-1]
    t = 0
    for i, v in enumerate(w):
        t += (i+1)*v
    return t


print(score(w))

p1, p2 = groups("22.in")
p1 = ints(p1.split("\n")[1:])
p2 = ints(p2.split("\n")[1:])


@cache
def play(p1, p2):
    p1, p2 = list(p1), list(p2)
    states = set()
    while p1 and p2:
        st = (tuple(p1), tuple(p2))
        if st in states:
            return 1, p1
        else:
            states.add(st)
            if (len(states) % 1000 == 0):
                print(len(states), len(p1)+len(p2))
        c1 = p1.pop(0)
        c2 = p2.pop(0)
        if c1 <= len(p1) and c2 <= len(p2):
            (w, _) = play(tuple(p1), tuple(p2))
        else:
            w = 1 if c1 > c2 else 2
        w, wc, lc = [0, (p1, c1, c2), (p2, c2, c1)][w]
        w.append(wc)
        w.append(lc)
    if p1:
        return 1, p1
    else:
        return 2, p2


(_, w) = play(tuple(p1), tuple(p2))
print(score(w))
