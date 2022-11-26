# pylint: disable=unused-wildcard-import
from utils import *

from cmath import tau, exp

dirs = {"e": 1+0j, "ne": exp(tau*1j/6), "nw": exp(2*tau*1j/6),
        "w": -1+0j, "sw": exp(4*tau*1j/6), "se": exp(5*tau*1j/6)}


def round_cplx(p):
    return round(p.real, ndigits=3) + 1j*round(p.imag, ndigits=3)


class ApproxSet():
    def __init__(self):
        self.data = {}

    def add(self, p):
        self.data[round_cplx(p)] = p

    def remove(self, p):
        del self.data[round_cplx(p)]

    def __contains__(self, p):
        return round_cplx(p) in self.data

    def __iter__(self):
        yield from self.data.values()

    def __len__(self):
        return len(self.data)


def parse(line):
    l = re.findall(r'[ns]?[ew]', line)
    assert "".join(l) == line
    return l


black = ApproxSet()

for l in inp_readlines():
    ds = parse(l)
    pos = 0j
    for d in ds:
        pos += dirs[d]
    if pos in black:
        black.remove(pos)
    else:
        black.add(pos)

print(black)
print(0, len(black))


def evolve(black):
    adj = ApproxSet()
    for b in black:
        for d in dirs.values():
            adj.add(b+d)
    new = ApproxSet()
    for p in adj:
        ns = 0
        for d in dirs.values():
            if p+d in black:
                ns += 1
        if p in black:
            if ns in [1, 2]:
                new.add(p)
        else:
            if ns == 2:
                new.add(p)
    return new


for i in range(100):
    black = evolve(black)
    print(i+1, len(black))
