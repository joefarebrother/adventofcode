from utils import *

lines = mapl(ints_in, inp_readlines())

def predict(seq):
    if all(x == 0 for x in seq):
        return 0 
    diffs = [b-a for a,b in windows(seq, 2)]
    nd = predict(diffs)
    return seq[-1]+nd

print("Part 1:", sum(predict(l) for l in lines))
print("Part 2:", sum(predict(l[::-1]) for l in lines))