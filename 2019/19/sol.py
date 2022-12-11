from intcode import *
from utils import *

prog = load_program()


def beam(x, y):
    return Machine(prog, [x, y]).run()[0]


grid = {}

# part 1
count = 0
for x in range(50):
    for y in range(50):
        count += beam(x, y)

print("Part 1:", count)

# part 2
x, y = 4, 3
while True:
    if beam(x, y):
        if beam(x+99, y-99):
            print("Part 2:", x*10000 + (y-99))
            break
        else:
            y += 1
    else:
        x += 1

'''
# sanity check:
x, y = x, y-100
for dx in range(-10,110):
  for dy in range(-10,110):
    print(beam(x+dx, y+dy), end='')
  print()
'''
