import intcode
from utils import *

outbuf = []
tiles = Grid({}, y_is_down=True)


def outfun(m, val):
    global outbuf, tiles
    outbuf.append(val)
    if len(outbuf) == 3:
        tiles[(outbuf[0], outbuf[1])] = outbuf[2]
        outbuf = []


def infun(m):
    tiles.draw([' ', '#', 'x', '=', 'o'])
    print(tiles[(-1, 0)])
    for pos in tiles:

        if tiles[pos] == 4:
            ballx = pos.real
        if tiles[pos] == 3:
            paddlex = pos.real

    return sign(ballx-paddlex)


m = intcode.Machine(None, infun, outfun)

m.prog[0] = 2

m.run()

print(tiles[(-1, 0)])
