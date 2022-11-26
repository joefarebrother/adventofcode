# pylint: disable=unused-wildcard-import
from utils import *
import sys
sys.setrecursionlimit(10000)

cups = ints("364289715")  # real
# cups = ints("389125467")  # test

mx = max(cups)


def wrap(i):
    return ((i-1) % mx) + 1


# for _ in range(100):
#     cur = cups[0]
#     picked = cups[1:4]
#     cups[1:4] = []
#     nxt = wrap(cur-1)
#     while nxt in picked:
#         nxt -= 1
#         nxt = wrap(nxt)
#     # print(cur, picked, nxt)
#     nidx = cups.index(nxt)+1
#     cups = cups[:nidx] + picked + cups[nidx:]
#     cups = cups[1:]+[cur]
#     print("".join([str(c) for c in cups]))

# oneidx = cups.index(1)
# cups = cups[oneidx:] + cups[:oneidx]
# print("".join([str(c) for c in cups[1:]]))

cups = ints("364289715")  # real
# cups = ints("389125467")  # test

cupslen = 1000000
# cupslen = len(cups)

for i in range(len(cups), cupslen):
    cups.append(i+1)

assert len(cups) == cupslen
mx = max(cups)
print(mx, cupslen)
assert mx == cupslen

nxt = {cups[-1]: cups[0]}

c = iter(cups)
next(c)
for p, n in zip(cups, c):
    nxt[p] = n

cur = cups[0]

print("Starting part 2")
iters = 10000000
# iters = 10

for i in range(iters):
    fst = nxt[cur]
    mid = nxt[fst]
    lst = nxt[mid]

    nxtnum = wrap(cur-1)
    while nxtnum in [fst, mid, lst]:
        nxtnum = wrap(nxtnum-1)

    nxt[cur] = nxt[lst]
    nxt[lst] = nxt[nxtnum]
    nxt[nxtnum] = fst

    cur = nxt[cur]

    if i % 10000 == 0:
        print(i, cur, nxtnum)

ans = (nxt[1], nxt[nxt[1]])
print(ans)
print(math.prod(ans))
