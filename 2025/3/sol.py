from utils import *

rows = inp_readlines()

def max_jolts(row):
    i,res = max(enumerate(row[:-12+1]), key=lambda ix: ix[1])
    for j in range(1,12):
        sub = row[i+1:] if j==11 else row[i+1:-12+j+1]
        printx(row, i, j, res, sub)
        i,nx = max(enumerate(sub, start=i+1), key=lambda ix: ix[1])
        res += nx
    printx(row, res)
    return int(res)

print(sum(map(max_jolts, rows)))