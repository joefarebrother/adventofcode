from utils import *

ranks = "A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2".split(", ")

new_ranks = "A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J".split(", ")


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

class Hand:
    def __init__(self, line):
        hand, bid = line.split()
        self.bid = int(bid)
        self.hand = hand 

    def kind(self):
        return kind(self.hand)
    
    def key(self):
        return self.kind(), mapl(lambda x: 10-ranks.index(x), self.hand)
    
    def kind_with_jokers(self):
        h = self.hand
        return max(kind(h.replace("J", c)) for c in new_ranks[:-1])
    
    def keyj(self):
        return self.kind_with_jokers(), mapl(lambda x: 10-new_ranks.index(x), self.hand)
    
    def __repr__(self):
        return f"{self.hand} {self.bid}"
    
hands = [Hand("A 0")] + sorted(mapl(Hand, inp_readlines()), key=Hand.key)
print(hands)

print("Part 1:", sum(h.bid*i for i,h in enumerate(hands)))

hands = [Hand("A 0")] + sorted(mapl(Hand, inp_readlines()), key=Hand.keyj)
print(hands)

print("Part 2:", sum(h.bid*i for i,h in enumerate(hands)))