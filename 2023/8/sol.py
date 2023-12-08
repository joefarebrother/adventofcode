from utils import *

inp = inp_readlines()
instr = inp[0]
gr1 = inp[2:]

cur = "AAA"
gr = {}
for line in gr1:
    i, o1, o2 = match(r'(...) = \((...), (...)\)', line)
    gr[i] = (o1, o2)

# steps = 0
# while cur != "ZZZ":
#     print(steps, cur)
#     cur = gr[cur][{"L":0,"R":1}[instr[steps%len(instr)]]]
#     steps += 1

# print("Part 1:", steps)

def time_to_z(node):
    steps = 0
    cur = node 
    while cur[-1] != "Z":
        cur = gr[cur][{"L":0,"R":1}[instr[steps%len(instr)]]]
        steps += 1
    return steps, (cur,steps%len(instr))

def next_node(nodeidx):
    node, idx = nodeidx 
    return gr[node][{"L":0,"R":1}[instr[idx%len(instr)]]], ((idx+1)%len(instr))

@cache
def period_and_init_and_uniq_zs(nodeidx):
    seen = {}
    zs = {}
    step = 0
    while True:
        #print(nodeidx)
        if nodeidx[0][-1] == "Z":
            zs[nodeidx] = step
        if nodeidx in seen:
            p = seen[nodeidx]
            print(nodeidx, step, p)
            return step-p, step, zs 
        seen[nodeidx] = step
        nodeidx = next_node(nodeidx)
        step += 1
        assert step % len(instr) == nodeidx[1]

res = {}
for n in gr:
    if n[-1] == "A":
        res[n] = period_and_init_and_uniq_zs((n,0))
        print(n, res[n])

x = math.lcm(*[p for (p,_,_) in res.values()]) # input follows special case making this work 

print("Part 2:", x)