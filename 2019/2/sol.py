from utils import *

initprog = list(map(int, inp_readall().split(",")))


def debug(prog, pc):
    i = 0
    while prog[i] != 99:
        print(str(prog[i:i+4]) + (" <- " if i == pc else ""))
        i += 4
    print(prog[i:i+1])
    print(prog[i+1:])
    print()
    print()


def run(noun, verb):
    prog = initprog[:]
    prog[1] = noun
    prog[2] = verb

    pc = 0
    while True:
        op = prog[pc]
        #debug(prog, pc)
        if op == 1:
            prog[prog[pc+3]] = prog[prog[pc+1]] + prog[prog[pc+2]]
        elif op == 2:
            prog[prog[pc+3]] = prog[prog[pc+1]] * prog[prog[pc+2]]
        elif op == 99:
            return prog[0]
        else:
            debug(prog, pc)
            raise Exception("oh no")
        pc += 4


print("Part 1:", run(12, 2))
for noun in range(1, 100):
    for verb in range(1, 100):
        if (run(noun, verb) == 19690720):
            print("Part 2:", 100*noun+verb)
            exit()
