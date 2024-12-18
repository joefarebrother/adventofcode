from utils import *

inp = ints_in(inp_readall())
regs = inp[:3]
prog=inp[3:]



def combo(arg):
    if arg < 4:
        return arg 
    else:
        return regs[arg-4] 
    
ip = 0
out = []

def step(op,arg):
    global ip 

    if op == 0:
        regs[0] >>= combo(arg)

    if op == 1:
        regs[1] ^= arg 

    if op == 2:
        regs[1] = combo(arg)%8

    if op == 3:
        if regs[0] != 0:
            ip = arg-2 

    if op == 4:
        regs[1] ^= regs[2]

    if op == 5:
        out.append(combo(arg)%8)

    if op == 6:
        regs[1] = regs[0] >> combo(arg)

    if op == 7:
        regs[2] = regs[0] >> combo(arg)

    ip += 2

def run():
    global ip,out
    ip = 0
    out = []
    while ip+1 < len(prog):
        step(prog[ip],prog[ip+1])
    return out 

run()

print("Part 1:", ",".join(mapl(str,out)))

# a = 0
# while True:
#     regs = [a,0,0]
#     if run() == prog:
#         break 
#     a += 1
 
# print("Part 2:", a)

# bst,4, b = a %8
# bxl,1, b ^= 1
# cdv,5, c = a >> b
# bxl,5, b ^= 5
# bxc,   b ^ c
# out,5, out b %8
# adv,3, a >>= 3
# bnz,0  bnz


def run_to_out(a):
    global regs 
    global ip 
    global out 
    ip = 0 
    regs = [a,0,0]
    out = [] 

    while not out:
        step(prog[ip],prog[ip+1])

    return out[0]

poss_ra = {0} 
for p in prog[::-1]:
    new_poss_ra = set()
    for a,ra in itertools.product(range(8), poss_ra):
        nra = ra*8+a
        if p == run_to_out(nra):
            new_poss_ra.add(nra)
            #print(ra, p, nra, new_poss_ra)
    poss_ra = new_poss_ra

ra = min(poss_ra)
regs = [ra,0,0]
res = run()
assert res == prog, (res,prog)


print("Part 2:", ra)