from utils import *

ranks = "A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2".split(", ")

new_ranks = "A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J".split(", ")

def parse(line):
    hand, bid = line.split()
    return (hand, int(bid))

def kind(h):
    c = Counter(h)
    rc = inv_mapping(c)
    if 5 in rc:
        return 10
    if 4 in rc:
        return 9 
    if 3 in rc and 2 in rc:
        return 8
    if 3 in rc:
        return 7 
    if 2 in rc:
        if len([x for x in c if c[x]==2]) == 2:
            return 6
        return 5
    return 4

def key(h):
    return kind(h), mapl(lambda x: 10-ranks.index(x), h)

def kindj(h):
    return max(kind(h.replace("J", c)) for c in new_ranks[:-1])

def keyj(h):
    return kindj(h), mapl(lambda x: 10-new_ranks.index(x), h)
    


raw_hands = mapl(parse, inp_readlines())
hands = [(0,0)] + sorted(raw_hands, key=lambda hb: key(hb[0]))

print("Part 1:", sum(hb[1]*i for i,hb in enumerate(hands)))

hands = [(0,0)] + sorted(raw_hands, key=lambda hb: keyj(hb[0]))

print("Part 2:", sum(hb[1]*i for i,hb in enumerate(hands)))