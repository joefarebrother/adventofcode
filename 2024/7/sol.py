from utils import *


eqs = []
for line in inp_readlines():
    nums = ints_in(line)
    eqs.append((nums[0], tuple(nums[1:])))

part2 = False
def possible(tar, eq):
    last = eq[-1]
    if len(eq) == 1:
        return tar == last
    if tar < last:
        return False
    if tar % eq[-1] == 0 and possible(tar//eq[-1], eq[:-1]):
        return True 
    if part2 and str(tar).endswith(strlast:=str(last)) and possible(tar//(10**len(strlast)), eq[:-1]):
        return True
    return possible(tar-last, eq[:-1])

print("Part 1:", sum(t for t,eq in eqs if possible(t,eq)))
part2=True
print("Part 2:", sum(t for t,eq in eqs if possible(t,eq)))