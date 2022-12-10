from utils import *

prog = inp_readlines()


def run(maxcyc):
    img = [[]]
    pc = 0
    x = 1
    waiting = False

    for cyc in range(maxcyc):
        instr = prog[pc]
        if instr == "noop":
            pc += 1
        else:
            if waiting:
                waiting = False
                pc += 1
                x += ints_in(instr)[0]
            else:
                waiting = True

        pix = mod_inc(cyc+1, 40)
        if -1 <= pix-x <= 1:
            img[-1].append("#")
        else:
            img[-1].append(".")
        if cyc % 40 == 39:
            img.append([])
    print(x, maxcyc)
    return x*maxcyc, Grid(img)


res = sum(run(x)[0] for x in [20, 60, 100, 140, 180, 220])
print(res)

_, img = run(240)
img.draw()
if not is_ex:
    print(input())
