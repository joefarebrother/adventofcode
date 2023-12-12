from utils import *

rows = []
for line in inp_readlines():
    r,n = line.split(" ")
    rows.append((r, tuple(ints_in(n))))

@cache
def ways(desc, nums, in_block=False):
    printx("call", desc, nums, in_block)
    if len(desc) == 0:
        return 0 if any(nums) else 1
    if len(nums) == 0:
        printx(desc, nums, in_block, 0 if "#" in desc else 1)
        return 0 if "#" in desc else 1
    
    fst_chr = desc[0]
    fst_num = nums[0]
    
    res = 0
    if fst_chr in "#?":
        if fst_num > 0:
            res += ways(desc[1:], (fst_num-1,)+nums[1:], True)
    if fst_chr in ".?":
        if not in_block:
            res += ways(desc[1:], nums, False)
        else:
            if fst_num == 0:
                res += ways(desc[1:], nums[1:], False)
    printx(desc, nums, in_block, res)
    return res 

tot = 0
for desc,nums in rows:
    tot += ways(desc, nums)

print("Part 1:", tot)

tot=0
for desc,nums in rows:
    tot += ways("?".join([desc]*5), nums*5)

print("Part 2:", tot)