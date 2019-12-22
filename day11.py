import intcode
from utils import *

painted = {0j: 1} # change to 0 for part 1
z = 0j

dir = 1j

outbuf = []

def infun(m):
  global painted
  return painted[z] if z in painted else 0

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

draw_grid(painted, [' ', '#'], flipy=True)

  
