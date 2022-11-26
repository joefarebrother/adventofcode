import intcode
from utils2020 import Grid

painted = Grid({0j: 1})  # change to {0j: 0} for part 1
z = 0j

dir = 1j

outbuf = []


def infun(m):
    global painted
    return painted[z] or 0


def outfun(m, val):
    global outbuf, z, dir, painted
    outbuf.append(val)
    if len(outbuf) == 2:
        newcol = outbuf[0]
        turn = outbuf[1]
        painted[z] = newcol
        dir *= (1j if turn == 0 else -1j)
        z += dir
        outbuf = []


mach = intcode.Machine("input11", infun, outfun)


mach.run()

painted.draw()
