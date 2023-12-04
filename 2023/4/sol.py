from utils import *

class Card:
    def __init__(self, line):
        n, row = line.split(":")
        w, have = row.split("|")
        self.id = ints_in(n)[0]
        self.win = ints_in(w)
        self.have = ints_in(have)

    def winning(self):
        n = 0
        for w in self.win:
            if w in self.have:
                n += 1
        return n
    
    def value(self):
        n = self.winning()

        return 0 if n == 0 else 1<<(n-1)
    
    def win_copies(self, amts):
        n = self.winning()

        for i in irange(n):
            amts[self.id+i] += amts[self.id]
    
cs = mapl(Card, inp_readlines())

amts = [0]+[1 for c in cs]

print("Part 1:", sum(c.value() for c in cs))

for c in cs:
    c.win_copies(amts)

print("Part 2:", sum(amts))