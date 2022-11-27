from intcode import Machine
from utils import *

grid = [[]]


def outfun(m, v):
    print(chr(v), end="")
    if v == 10:
        grid.append([])
    else:
        grid[-1].append(chr(v))


mach = Machine(None, out=outfun)

mach.run()
grid = grid[:-2]

grid_ = Grid(grid)

tot = 0
for (pos, c) in grid_.items():
    if c == '#' and all([p in grid_ and grid_[p] == '#' for p in neighbours(pos)]):
        tot += int(pos.real*pos.imag)

print(tot)

instrs = '\n'.join([
    "A,B,A,B,C,C,B,C,B,A",
    "R,12,L,8,R,12",
    "R,8,R,6,R,6,R,8",
    "R,8,L,8,R,8,R,4,R,4",
    "n\n"
])
print([ord(c) for c in instrs])

"8,L,8,R,8,R,4,R,8,8,L,8,R,8,R,4,R,"

mach = Machine(None, inp=instrs, out=outfun)
mach.prog[0] = 2

mach.run()
print(ord(grid[-1][-1]))

# Automated command finding:

for p, v in grid_.items():
    if v == '^':
        pos = p
        dir = -1j


def ok(z):
    return grid_[z] == '#'


cmd = []
n = 0
while True:
    if ok(pos+dir):
        n += 1
        pos += dir
    elif ok(pos+1j*dir):
        cmd += [n, 'R']
        n = 0
        dir *= 1j
    elif ok(pos-1j*dir):
        cmd += [n, 'L']
        n = 0
        dir *= -1j
    else:
        cmd += [n]
        break

cmd = cmd[1:]
print(cmd)


def cmdstr(cmd):
    return ','.join(map(str, cmd))


for Aend in range(1, len(cmd)):
    A = cmd[:Aend]
    if len(cmdstr(A)) > 20:
        break

    for Bstart in range(Aend, len(cmd)):
        for Bend in range(Bstart+1, len(cmd)):
            B = cmd[Bstart:Bend]
            if len(cmdstr(B)) > 20:
                break

            for Cstart in range(Bend, len(cmd)):
                for Cend in range(Cstart+1, len(cmd)):
                    C = cmd[Cstart:Cend]
                    if len(cmdstr(C)) > 20:
                        break

                    #print(A, B, C)
                    cmd2 = []
                    i = 0
                    while True:
                        if i+len(A) <= len(cmd) and cmd[i:i+len(A)] == A:
                            i += len(A)
                            cmd2 += ['A']
                        elif i+len(B) <= len(cmd) and cmd[i:i+len(B)] == B:
                            i += len(B)
                            cmd2 += ['B']
                        elif i+len(C) <= len(cmd) and cmd[i:i+len(C)] == C:
                            i += len(C)
                            cmd2 += ['C']
                        elif i < len(cmd):
                            #print(A, B, C, cmd2)
                            break
                        else:
                            if len(cmdstr(cmd2)) > 20:
                                break

                            print("Possibility found!\n")
                            instr = '\n'.join(
                                mapl(cmdstr, [cmd2, A, B, C]) + ['n', ''])
                            print(instr)
                            instrs = mapl(ord, instr)

                            mach = Machine(None, inp=instrs, out=outfun)
                            mach.prog[0] = 2

                            mach.run()
                            print()
                            print(ord(grid[-1][-1]))
                            exit()
