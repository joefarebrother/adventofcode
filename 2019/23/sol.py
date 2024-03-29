from intcode import *
from utils import *

prog = load_program()


idle_count = 0
nat_history = [-1]


def inpfun(m):
    global idle_count, nat_history
    if all([len(m.inp) == 0 for m in machines]):
        idle_count += 1
        if idle_count > 10000:
            print("idle")
            machines[0].send_input(nat)
            idle_count = 0
            print(nat)
            if nat[1] == nat_history[-1]:
                print("Part 2:", nat[1])
                exit()
            nat_history += [nat[1]]
    else:
        idle_count = 0

    if len(m.inp) == 0:
        return -1
    else:
        return m.inp.pop(0)


nat = [0, 0]

have_p1 = False


def outfun(m, v):
    global nat, have_p1
    m.out += [v]
    if len(m.out) == 3:
        if m.out[0] == 255:
            if not have_p1:
                print("Part 1:", m.out[2])
                have_p1 = True
            nat = m.out[1:]
        else:
            machines[m.out[0]].send_input(m.out[1:])
        m.out = []


machines = [Machine(prog, inpfun, outfun, name=i) for i in range(50)]

for i, m in enumerate(machines):
    m.send_input(i)


while True:
    for m in machines:
        m.step()
