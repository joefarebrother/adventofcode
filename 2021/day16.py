from dataclasses import field
from utils import *

hexd = {hex(n)[2]: bin(n)[2:].rjust(4, "0") for n in range(16)}
printx(hexd)
inp = readlines(16)[0]
ih = ""
for d in inp:
    ih += hexd[d.lower()]
inp = ih
printx(inp)


@ dataclass
class Packet:
    version: int
    ty: int
    lit: int = 0
    sub: list = field(default_factory=list)

    def versum(self):
        return self.version + sum(s.versum() for s in self.sub)

    def eval(self):
        """

    Packets with type ID 0 are sum packets - their value is the sum of the values of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
    Packets with type ID 1 are product packets - their value is the result of multiplying together the values of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
    Packets with type ID 2 are minimum packets - their value is the minimum of the values of their sub-packets.
    Packets with type ID 3 are maximum packets - their value is the maximum of the values of their sub-packets.
    Packets with type ID 5 are greater than packets - their value is 1 if the value of the first sub-packet is greater than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
    Packets with type ID 6 are less than packets - their value is 1 if the value of the first sub-packet is less than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
    Packets with type ID 7 are equal to packets - their value is 1 if the value of the first sub-packet is equal to the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.

        """
        ty = self.ty
        sub = [s.eval() for s in self.sub]
        printx(ty, sub)
        if ty == 0:
            return sum(sub)
        elif ty == 1:
            return math.prod(sub)
        elif ty == 2:
            return min(sub)
        elif ty == 3:
            return max(sub)
        elif ty == 4:
            return self.lit
        elif ty == 5:
            return int(sub[0] > sub[1])
        elif ty == 6:
            return int(sub[0] < sub[1])
        elif ty == 7:
            return int(sub[0] == sub[1])


def rbin(x):
    return int(x, 2)


def parse(off):
    ver = rbin(inp[off:off+3])
    ty = rbin(inp[off+3:off+6])
    if ty == 4:
        off += 6
        lit = 0
        grp = "1"
        while grp[0] == "1":
            grp = inp[off:off+5]
            lit *= 16
            lit += rbin(grp[1:])
            off += 5
        return Packet(ver, ty, lit), off
    else:
        mode = inp[off+6]
        sub = []
        if mode == "0":
            ln = rbin(inp[off+7:off+7+15])
            printx(mode, off, inp[off+7:off+7+15], ln)
            off += 7+15
            endoff = off+ln
            while off < endoff:
                p, off = parse(off)
                sub.append(p)
                assert off <= endoff
        else:
            ln = rbin(inp[off+7: off+7+11])
            printx(mode, off, inp[off+7: off+7+11], ln)
            off += 7+11
            for _ in range(ln):
                p, off = parse(off)
                sub.append(p)
        return Packet(ver, ty, sub=sub), off


root, _ = parse(0)
print("Part 1:", root.versum())
print("Part 2:", root.eval())
