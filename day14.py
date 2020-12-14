# pylint: disable=unused-wildcard-import
from utils import *

mem = defaultdict(int)
maskv = 0
maskm = 0
mask = None
mtab = str.maketrans("X01", "100")

inp = [l.split(" = ") for l in readlines("14.in")]

for (loc, val) in inp:
    if loc == "mask":
        print(val.count("X"))
        maskm = int(val.translate(mtab), 2)
        maskv = int(val.replace("X", "0"), 2)
    else:
        (adr,) = ints_in(loc)
        rval = int(val) & maskm | maskv
        mem[adr] = rval

print(mem)
print(sum(mem.values()))
mask = None

mem = defaultdict(int)


def trans(adr):
    base = (adr | maskv) & ~maskm
    for flo in range(1 << mask.count("X")):
        res = base
        for (idx, c) in enumerate(reversed(mask)):
            if c == "X":
                res |= ((flo & 1) << idx)
                flo >>= 1
        yield res


for (loc, val) in inp:
    if loc == "mask":
        maskm = int(val.translate(mtab), 2)
        maskv = int(val.replace("X", "0"), 2)
        mask = val
    else:
        (adr,) = ints_in(loc)
        for radr in trans(adr):
            mem[radr] = int(val)

print(len(mem))
print(sum(mem.values()))
