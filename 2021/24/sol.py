from utils import *
import sys

m = None
# if not is_ex and len(sys.argv) == 2:
#     m = sys.argv[1]
#     sys.argv = [sys.argv[0]]

inp = inp_readlines()

prog = [l.split() for l in inp]

ops = {"add": (lambda a, b: a+b),
       "mul": (lambda a, b: a*b),
       "div": (lambda a, b: int(a/b)),
       "mod": (lambda a, b: a % b),
       "eql": (lambda a, b: int(a == b))}


def reg(regs, r):
    return regs["wxyz".find(r)]


def sreg(regs, r, v):
    return modify_idx(regs, "wxyz".find(r), v)


def run(inp):
    regs = (0, 0, 0, 0)
    inp = iter(inp)

    for instr in prog:
        op = instr[0]
        if op == "inp":
            regs = sreg(regs, instr[1], next(inp))
        else:
            op, a, b, = instr
            b = int(b) if numeric(b) else reg(regs, b)
            regs = sreg(regs, a, ops[op](reg(regs, a), b))
    return regs[-1] == 0


if is_ex:
    print(69)
    exit()

if m:
    print(run(m))
    exit()

cur = {}
i = 0

grps = []
for ins in prog:
    if ins[0] == "inp":
        grps.append([])
    grps[-1].append(ins)

# each group is of the form
# inp w
# mul x 0
# add x z
# mod x 26
# div z [1 or 26]
# add x A
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y B
# mul y x
# add z y
# i.e. (maybe pop z, if in=z[-1]+A then z.push(in+B))

grinstrs = []
for g in grps:
    pops = g[4][-1] == "26"
    A = int(g[5][-1])
    B = int(g[-3][-1])
    grinstrs.append((pops, A, B))

print(grinstrs)


def complete(n):
    n = iter(n)
    m = [0]*14
    stk = []
    for i, (pops, A, B) in enumerate(grinstrs):
        if pops:
            j, jB = stk.pop()
            cor = m[j]+jB+A
            if cor in irange(1, 9):
                m[i] = cor
            else:
                return None
        else:
            m[i] = next(n)
            stk.append((i, B))
    return m


for m in it.product(irange(9, 1, -1), repeat=7):
    m = complete(m)
    if m:
        print("Part 1:", "".join(str(c) for c in m))
        assert run(m)
        break

for m in it.product(irange(1, 9), repeat=7):
    m = complete(m)
    if m:
        print("Part 2:", "".join(str(c) for c in m))
        assert run(m)
        break
