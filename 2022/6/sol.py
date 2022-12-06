from utils import *

inp = inp_readall()


def find(unq):
    for i, m in enumerate(windows(inp, unq)):
        if is_uniq(m):
            return i+unq


print("Part 1:", find(4))
print("Part 2:", find(14))
