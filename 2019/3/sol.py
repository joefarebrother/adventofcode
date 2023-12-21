from utils import Rectangle, inp_readlines, man_dist


def process(line):
    wires = []
    pos = 0j
    totlen = 0
    for wire in line.split(','):
        oldpos = pos
        dir = wire[0]
        len = int(wire[1:])
        if dir == 'R':
            pos += len
        elif dir == 'L':
            pos -= len
        elif dir == 'U':
            pos += len*1j
        elif dir == 'D':
            pos -= len*1j
        wires.append((Rectangle(oldpos, pos), oldpos, totlen))
        totlen += len
    return wires


def isHor(wire):
    (rec, _, _) = wire
    return rec.height == 1


def isVer(wire):
    (rec, _, _) = wire
    return rec.width == 1


def intersect(w1, w2):
    if isHor(w1) and isHor(w2):
        return None
    if isVer(w1) and isVer(w2):
        return None

    (rec1, p1, len1) = w1
    (rec2, p2, len2) = w2

    rec = rec1 & rec2
    if not rec:
        return None

    intp = rec.opposite_corners()[0]

    return (intp, int(len1+abs(intp-p1)+len2+abs(intp-p2)))


wires = []

for line in inp_readlines():
    wires.append(process(line))

inters = [i for w1 in wires[0] for w2 in wires[1] for i in [intersect(w1, w2)] if i not in [(0, 0), None]]

print("Part 1:", min(man_dist(p) for (p, d) in inters))
print("Part 2:", min(d for (p, d) in inters))
