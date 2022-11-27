from utils import *
from intcode import Machine
from time import sleep
import sys

known_tiles = Grid({0j: 1})

next_pos = 0j
target_pos = None


def draw(pos):
    #print(chr(27) + "[2J")
    old = known_tiles[pos]
    known_tiles[pos] = 4
    print()
    known_tiles.draw([' ', '.', '█', 'o', 'D'])
    print(flush=True)
    sleep(0.05)
    known_tiles[pos] = old


#mach = Machine(None, inpfun, outfun)
mach = Machine(None, [])


class MGraph(AbGraph):  # floodfill
    def adj(self, node):
        global mach, target_pos, known_tiles

        for i, dir in enumerate([0, 1j, -1j, -1, 1]):
            if i == 0:
                continue
            npos = node+dir
            mach.send_input(i)
            out = mach.run_until_input()[-1]
            if out == 0:
                known_tiles[npos] = 2
            elif out == 1:
                known_tiles[npos] = 1
                yield (npos)
                mach.send_input([0, 2, 1, 4, 3][i])
            elif out == 2:
                known_tiles[npos] = 3
                target_pos = npos
                yield (npos)
                mach.send_input([0, 2, 1, 4, 3][i])


MGraph().DFS(0j)


draw(0j)

print(target_pos)

# now pathfind from target: breadth-first


maze = FGraph(lambda p: neighbours(p) if known_tiles[p] != 2 else [])

print("part 1: ", maze.BFS(target_pos, 0j)[1])
print("part 2: ", maze.BFS(target_pos)[1])
