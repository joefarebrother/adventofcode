from utils import *

prog = inp_readlines()


def run():
    img = []
    strength = 0
    pc = 0
    x = 1
    waiting = False

    for cyc in irange(240):
        instr = prog[pc]

        if cyc % 40 == 20:
            print(cyc, x, instr, waiting)
            strength += cyc*x

        pix = (cyc-1) % 40
        if -1 <= pix-x <= 1:
            img.append("#")
        else:
            img.append(".")

        if instr == "noop":
            pc += 1
        else:
            if waiting:
                waiting = False
                pc += 1
                x += ints_in(instr)[0]
            else:
                waiting = True

    img = list(chunks(img, 40))
    return strength, Grid(img)


strength, img = run()
print("Part 1:", strength)
img.draw()
if not is_ex:
    print("Part 2:", input())
