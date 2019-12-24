from collections import deque
from heapq import heappush, heappop
import math

def block_char():
  return '█'

def draw_grid(grid, symbols=None, flipx=False, flipy=False):
  res=''

  if symbols == None:
    symbols = {0: ' ', 1: '█'}

  if type(symbols) != dict:
    symbols = {i:v for i, v in enumerate(symbols)}

  if type(grid) == list :
    for y in (range(len(grid)) if not flipy else range(len(grid)-1, -1, -1)):
      for x in (range(len(grid[y])) if not flipy else range(len(grid[y])-1, -1, -1)):
        elt = grid[y][x]
        sym = symbols[elt] if elt in symbols else str(elt)[0]
        res += sym
      res += '\n'

  elif type(grid) == dict:
    coords = grid.keys()
    if len(coords) == 0:
      return
    if type(list(coords)[0]) == complex:
      xcoords = [int(z.real) for z in coords]
      ycoords = [int(z.imag) for z in coords]
    else:
      xcoords = [x for (x, y) in coords]
      ycoords = [y for (x, y) in coords]

    for y in (range(min(ycoords), max(ycoords)+1) if not flipy else range(max(ycoords), min(ycoords)-1, -1)):
      for x in (range(min(xcoords), max(xcoords)+1) if not flipx else range(max(xcoords), min(xcoords)-1, -1)):
        if type(list(coords)[0]) == complex:
          elt = grid[(x+y*1j)] if (x+y*1j) in grid else ' '
        else:
          elt = grid[(x, y)] if (x, y) in grid else ' '
        sym = symbols[elt] if elt in symbols else str(elt)[0]
        res += sym
      res += '\n'

  print(res)

def grid_to_cplx(grid):
  cgrid = {}
  for y, line in enumerate(grid):
    for x, c in enumerate(line):
      cgrid[x+y*1j] = c

  return cgrid

def sign(x):
  if x < 0:
    return -1
  if x > 0:
    return 1
  return 0

gcd = math.gcd
    
def lcm(a, b):
    return a * b / gcd(a, b)

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def mod_inv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def clear_screen():
  print(chr(27) + "[2J")

def map(f, xs):
  return [f(x) for x in xs]

def neighbours(p):
  return [p+1j**dir for dir in range(4)]

def ident(x):
  return x

def BFS(start, adjfun, end=None, key=ident):
  queue = deque([(start, 0)])
  visited = {key(start)}
  d = 0
  while len(queue) > 0:
    p, d = queue.popleft()
    
    if (callable(end) and end(p)) or end == p:
      BFS.queue = None
      BFS.dist = 0
      return (d, True)
    BFS.queue = queue
    BFS.dist = d
    next = adjfun(p)
    if next != None:
      for n in next:
        if key(n) in visited:
          continue
        visited |= {key(n)}
        queue += [(n, d+1)]
  BFS.queue = None
  BFS.dist = 0
  return (d, False)

def astar(start, adjfun, end=None, key=ident, h=lambda _:0):
  pqueue = [(h(start), 0, 0, start)]
  i = 0
  dists = {key(start):0}
  while len(pqueue) > 0:
    _, d, _, p = heappop(pqueue)
    if dists[key(p)] < d:
      continue

    if (callable(end) and end(p)) or end == p:
      astar.pqueue = None
      astar.dists = None
      astar.dist = 0
      return d

    astar.pqueue = pqueue
    astar.dists = dists
    astar.dist = d
    next = adjfun(p)
    if next != None:
      for n, nd in next:
        if key(n) in dists and dists[key(n)] <= d+nd:
          continue
        dists[key(n)] = d+nd
        i += 1
        heappush(pqueue, (d+nd+h(n), d+nd, i, n))

  astar.pqueue = None
  astar.dists = None
  astar.dist = 0
  if end != None:
    return None
  else:
    return dists

dijkstra = astar




