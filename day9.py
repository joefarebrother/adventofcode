# pylint: disable=unused-wildcard-import
from utils import *
import itertools

nums = ints(readlines("9.in"))
print(nums)

invalid = None

for (i, num) in enumerate(nums):
    if i < 25:
        continue
    before = nums[i-25: i]
    found = True
    for c in itertools.combinations(before, 2):
        if sum(c) == num:
            found = False
            break
    if found:
        print("p1:", num)
        invalid = num
        break

for (lo, hi) in itertools.combinations(range(len(nums)+1), 2):
    rng = nums[lo:hi]
    if sum(rng) == invalid:
        print(min(rng), max(rng), "p2:", min(rng)+max(rng))
