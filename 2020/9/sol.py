# pylint: disable=unused-wildcard-import
from utils import *
import itertools

nums = ints(inp_readlines())
print(nums)

invalid = None

for (i, num) in enumerate(nums):
    if i < 25:
        continue
    before = nums[i-25: i]
    for c in itertools.combinations(before, 2):
        if sum(c) == num:
            break
    else:
        print("p1:", num)
        invalid = num
        break

for (lo, hi) in itertools.combinations(range(len(nums)+1), 2):
    rng = nums[lo:hi]
    if sum(rng) == invalid and min(rng) != max(rng):
        print(min(rng), max(rng), "p2:", min(rng)+max(rng))
