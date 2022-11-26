# pylint: disable=unused-wildcard-import
from utils import *

nums = [0] + sorted(ints(inp_readlines()))

diffs = [nums[i+1] - nums[i] for i in range(len(nums)-1)] + [3]
print(diffs)

print(diffs.count(1)*diffs.count(3))

ways = defaultdict(int)
ways[0] = 1
for i in nums[1:]:  # skip leading 0 added on earlier
    ways[i] = ways[i-1]+ways[i-2]+ways[i-3]

print(ways)
