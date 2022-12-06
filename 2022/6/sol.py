from utils import *

inp = inp_readall()

for i, m in enumerate(windows(inp, 4)):
    if len(set(m)) == 4:
        print(i+4)
        break

for i, m in enumerate(windows(inp, 14)):
    if len(set(m)) == 14:
        print(i+14)
        break
