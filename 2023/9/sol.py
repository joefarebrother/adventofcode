from utils import *

lines = mapl(ints_in, inp_readlines())

def predict(seq):
    if all(x == 0 for x in seq):
        return 0 
    diffs = [b-a for a,b in windows(seq, 2)]
    nd = predict(diffs)
    return seq[-1]+nd

def predict2(seq):
    if all(x == 0 for x in seq):
        return 0 
    diffs = [b-a for a,b in windows(seq, 2)]
    nd = predict2(diffs)
    return seq[0]-nd

print("Part 1:", sum(predict(l) for l in lines))
print("Part 2:", sum(predict2(l) for l in lines))