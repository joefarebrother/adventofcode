import intcode
from utils import *

outbuf = []
tiles = {}
def outfun(m, val):
  global outbuf, tiles
  outbuf.append(val)
  if len(outbuf) == 3:
    tiles[(outbuf[0], outbuf[1])] = outbuf[2]
    outbuf = []

def infun(m):
  print(tiles[(-1, 0)])
  draw_grid(tiles, [' ', '#', 'x', '=', 'o'])
  for x, y in tiles:
        
        if tiles[(x, y)] == 4:
          ballx = x
        if tiles[(x, y)] == 3:
          paddlex = x
  
  return sign(ballx-paddlex)
  


m = intcode.Machine("input13", infun, outfun)

m.prog[0] = 2

m.run()

print(tiles[(-1, 0)])

count = 0
for i in tiles:
  if tiles[i] == 2:
    count += 1

print(count)
