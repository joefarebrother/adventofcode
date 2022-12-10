# pylint: disable=unused-wildcard-import
from utils import *

nums = ints_in(inp_readall())

timestamps = defaultdict(lambda: t)
t = 1
for x in nums:
    last = x
    lastt = timestamps[x]
    timestamps[x] = t
    t += 1


while True:
    nxt = t-lastt-1
    last = nxt
    lastt = timestamps[nxt]
    timestamps[nxt] = t

    if t == 2020:
        print("Part 1:", t, len(timestamps), nxt)

    if t % 1000000 == 0:
        print(t, len(timestamps), nxt)

    if t == 30000000:
        print("Part 2:", t, len(timestamps), nxt)
        break

    t += 1
