# pylint: disable=unused-wildcard-import
from utils import *
import itertools

nums = ints(inp_readlines())
print(nums)

invalid = None

pre_len = 5 if is_ex else 25

for (i, num) in enumerate(nums):
    if i < pre_len:
        continue
    before = nums[i-pre_len: i]
    for c in itertools.combinations(before, 2):
        if sum(c) == num:
            break
    else:
        print("part 1:", num)
        invalid = num
        break

for (lo, hi) in itertools.combinations(range(len(nums)+1), 2):
    rng = nums[lo:hi]
    if sum(rng) == invalid and min(rng) != max(rng):
        print("part 2:", min(rng), max(rng), min(rng)+max(rng))
