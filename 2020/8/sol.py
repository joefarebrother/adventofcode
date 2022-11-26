# pylint: disable=unused-wildcard-import
from utils import *


def parse(l):
    return match(r'([a-z]{3}) ([+-]\d*)', l)


sprog = [parse(l) for l in inp_readlines()]


def run(prog):
    acc = 0
    pc = 0
    visited = set()
    while True:
        if pc in visited:
            return (False, acc)
        if pc == len(prog):
            return (True, acc)
        visited.add(pc)
        (op, arg) = prog[pc]
        if op == "acc":
            acc += arg
        elif op == "jmp":
            pc += arg
            continue
        pc += 1


print(run(sprog))

for (i, (instr, num)) in enumerate(sprog):
    if instr == "acc":
        continue
    nprog = [p for p in sprog]
    if instr == "jmp":
        nprog[i] = ("nop", num)
    else:
        nprog[i] = ("jmp", num)
    (end, res) = run(nprog)
    print(end, res, i)
    if end:
        print(res)
        break
