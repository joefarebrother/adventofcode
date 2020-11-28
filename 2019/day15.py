from utils import *
from intcode import Machine
from time import sleep

known_tiles = {0j: 1}

pos = 0j
next_pos = 0j
target_pos = None

visited = []
stack = ["fill"]

def draw(pos):
  print(chr(27) + "[2J")
  old = known_tiles[pos]
  known_tiles[pos] = 4
  print()
  draw_grid(known_tiles, [' ', '.', '█', 'o', 'D'])
  print(flush=True)
  sleep(0.05)
  known_tiles[pos] = old
  

#mach = Machine("input15", inpfun, outfun)
mach = Machine("input15", [])

def floodfill(mach, pos):
  global target_pos
  #invariant: we end on the same position we started
  if pos in visited:
    return
  #draw(pos)
  visited.append(pos)
  for i, dir in enumerate([0, 1j, -1j, -1, 1]):
    if i == 0:
      continue
    npos = pos+dir
    mach.send_input(i)
    out = mach.run_until_input()[-1]
    if out == 0:
      known_tiles[npos] = 2
    elif out == 1:
      known_tiles[npos] = 1
      floodfill(mach, npos)
      mach.send_input([0, 2, 1, 4, 3][i])
    elif out == 2:
      known_tiles[npos] = 3
      target_pos = npos
      floodfill(mach, npos)
      mach.send_input([0, 2, 1, 4, 3][i])

floodfill(mach, 0j)

draw(pos)

print(target_pos)

#now pathfind from target: breadth-first

max_d = 0

def adj(p):
  global max_d
  max_d = max(max_d, BFS.dist)
  if known_tiles[p] != 2:
    return neighbours(p)

'''
visited = []
queue = [(target_pos, 0)]
max_dist = 0
while len(queue) > 0:
  elt, dist = queue.pop(0)
  if elt == 0j: # uncomment for part 1
    print("part1: ", dist)
  max_dist = max(dist, max_dist)
  for dir in [1, 1j, -1, -1j]:
    next = elt+dir
    if known_tiles[next] != 2 and next not in visited:
      queue.append((next, dist+1))
  visited.append(elt)
'''

print("part1: ", BFS(target_pos, adj, 0j))
BFS(target_pos, adj)
print("part2: ", max_d)
      
