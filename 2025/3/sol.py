from utils import *

rows = inp_readlines()

def max_jolts(row, sel):
    i,res = -1,""
    for j in range(0,sel):
        sub = row[i+1:len(row)-sel+j+1]
        printx(row, i, j, res, sub)
        i,nx = max(enumerate(sub, start=i+1), key=lambda ix: ix[1])
        res += nx
    printx(row, res)
    return int(res)

print("Part 1:", sum(max_jolts(row, 2) for row in rows))
print("Part 2:", sum(max_jolts(row, 12) for row in rows))