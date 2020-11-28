

def process(line):
  wires = []
  x = 0
  y = 0
  totlen = 0
  for wire in line.split(','):
    oldpos = (x, y)
    dir = wire[0]
    len = int(wire[1:])
    if dir == 'R':
      x += len
    elif dir == 'L':
      x -= len
    elif dir == 'U':
      y += len
    elif dir == 'D':
      y -= len
    wires.append((oldpos, (x, y), totlen))
    totlen += len
  return wires

def isHor(wire):
  ((sx, sy), (ex, ey), _) = wire
  return sy == ey

def isVer(wire):
  ((sx, sy), (ex, ey), _) = wire
  return sx == ex

def intersect(w1, w2):
  if isHor(w1) and isHor(w2):
    return None
  if isVer(w1) and isVer(w2):
    return None
  if isVer(w1) and isHor(w2):
    w2, w1 = w1, w2
  
  ((sx1, y1), (ex1, _), len1) = w1
  ((x2, sy2), (_, ey2), len2) = w2

  if sx1 <= x2 and x2 <= ex1 and sy2  <= y1 and y1 <= ey2:
    return (x2, y1, len1+abs(x2-sx1)+len2+abs(y1-sy2))
  else:
    return None

wires = []

for line in open('input3').readlines():
  wires.append(process(line))

bestIntDist = None
for w1 in wires[0]:
  for w2 in wires[1]:
    inter = intersect(w1, w2)
    if inter and inter != (0, 0):
      (x, y, len) = inter
      if (not bestIntDist) or bestIntDist > len:
         bestIntDist = len 

print(bestIntDist) 

