# pylint: disable=unused-wildcard-import
from utils import *

instrs = readlines("12.in")

# Original version is in the commit history

pos = 0j
Dirs.F = Dirs.E

for l in instrs:
    c, n = l[0], int(l[1:])
    if c == "L":
        Dirs.F *= 1j**(n//90)
    elif c == "R":
        Dirs.F /= 1j**(n//90)
    else:
        pos += Dirs[c] * n
    print(l, pos, Dirs.F)

print(man_dist(pos))

pos = 0j
way = 10+1j

for l in instrs:
    c, n = l[0], int(l[1:])
    if c == "L":
        way *= 1j**(n//90)
    elif c == "R":
        way /= 1j**(n//90)
    elif c == "F":
        pos += way*n
    else:
        way += Dirs[c] * n
    print(l, pos, way)

print(man_dist(pos))
