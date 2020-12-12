# pylint: disable=unused-wildcard-import
from utils import *

instrs = readlines("12.in")

pos = 0j
dir = 1+0j

for l in instrs:
    c, n = l[0], int(l[1:])
    if c == "L":
        dir *= 1j**(n//90)
    elif c == "R":
        dir /= 1j**(n//90)
    else:
        pos += {"N": 1j, "E": 1, "S": -1j, "W": -1, "F": dir}[c] * n
    print(l, pos, dir)

print(int(abs(pos.real) + abs(pos.imag)))

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
        way += {"N": 1j, "E": 1, "S": -1j, "W": -1}[c] * n
    print(l, pos, way)

print(int(abs(pos.real) + abs(pos.imag)))
