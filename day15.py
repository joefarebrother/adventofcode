# pylint: disable=unused-wildcard-import
from utils import *

nums = ints_in(open("15.in").read())

# while True:
#     last = nums[-1]
#     for (i, x) in enumerate(reversed(nums)):
#         if i == 0:
#             continue
#         if x == last:
#             nums.append(i)
#             break
#     else:
#         nums.append(0)
#     print(len(nums), nums[-1])
#     if len(nums) == 15:
#         break

nums = [0, 3, 6]

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

    if True:
        print(t, len(timestamps), nxt)

    if t == 30000000:
        print(t, len(timestamps), nxt)
        break

    t += 1
