from utils import *

sys.setrecursionlimit(1000000000)

grid = Grid(0)

guard = complex(grid.index("^"))

nxt = {}
prv = defaultdict(list)

for p in grid:
    p = complex(p)
    if grid[p] == "#":
        continue
    for d in neighbours(0):
        d = complex(d)
        np = p+d 
        if grid[np] == "#":
            npd = (p,d*1j)
        else:
            npd = (p+d,d)
        nxt[p,d] = npd 
        prv[npd].append((p,d))

assert len(nxt) == (len(grid.indices("."))+1)*4 

# DFS label 
timestamp = 0
cur_cycle = 0
fwd_time_enter = {}
fwd_time_exit = {}

label_ = {}

def dfs(pd):
    global timestamp, cur_cycle 
    if pd in fwd_time_enter:
        return

    fwd_time_enter[pd] = timestamp 
    timestamp += 1

    npd = nxt[pd]
    if npd[0] not in grid:
        label_[pd] = ("edge",pd)
    else:
        dfs(npd)
        if npd not in fwd_time_exit:
            # cycle 
            label_[pd] = ("cycle", npd, cur_cycle)
        else:
            lnpd = label_[npd]
            if lnpd[0] == "cycle":
                if cur_cycle == lnpd[2]:
                    if pd == lnpd[1]:
                        cur_cycle += 1 
                else:
                    lnpd = ("tail",) + lnpd[1:]
            label_[pd] = lnpd

    fwd_time_exit[pd] = timestamp 
    timestamp += 1
        
def label(np):
    dfs(np)
    return label_[np]

# assert len(time_enter) == len(nxt), (len(time_enter), len(nxt))
# assert len(label) == len(nxt)

time_enter = {}
time_exit = {}
def dfs_rev(pd):
    global timestamp 
    if pd in time_enter:
        return
    
    assert pd in nxt, pd

    time_enter[pd] = timestamp 
    timestamp += 1

    for ppd in prv[pd]:
        dfs_rev(ppd)

    time_exit[pd] = timestamp 
    timestamp += 1




#assert len(time_enter) == len(nxt), (len(time_enter), len(nxt), list(set(time_enter)-set(nxt))[0])

def ancestor(a,b):
    """Returns true if A is an ancestor of B"""
    if b not in time_enter:
        lb = label(b)
        dfs_rev(lb[1])
    if a not in time_enter:
        return False
    if time_enter[b] <= time_enter[a] and time_exit[a] <= time_exit[b]:
        return True 
    la = label(a)
    lb = label(b)
    if la[0] == "cycle" and la == lb:
        return True 
    return False 

#print([p for p in nxt if label[p] == ('cycle', (P(28, 31), P(0, 1)), 0)])

# for p in nxt:
#     if nxt[p][0] in grid:
#         assert ancestor(p, nxt[p]), (p, nxt[p], label[p], label[nxt[p]], time_enter[nxt[p]], time_enter[p], time_exit[p], time_exit[nxt[p]])

    # this assert breaks linear time bound
    # if label[p][0] == "cycle":
    #     np = p
    #     for _ in range(len(nxt)):
    #        np = nxt[np]
    #        if np == p:
    #            break
    #     else:
    #         assert False 

def loops_with_wall(p):
    # this must be constant time 
    del_nodes = [(p,1j**k) for k in range(4)]
    heads = [npd for pd in del_nodes for npd in prv[pd] if npd not in del_nodes] # constant - bounded by 8

    seen_heads = set()
    st = (guard, 1j)

    while True: # constant - loops at most len(heads) times
        oh = [h for h in heads if ancestor(st, h)]
        if oh:
            bh = oh[0]
            for h2 in oh[1:]:
                if ancestor(h2,bh):
                    bh = h2 
            if bh in seen_heads:
                return True
            np,d = bh 
            seen_heads.add(bh)
            st = np, d*1j
            
            continue

        
        if label(st)[0] == "edge":
            return False 
        return True 
        
pos = set()
pd = (complex(guard), -1j)
while pd[0] in grid:
    pos.add(pd[0])
    pd = nxt[pd]

print("Part 1:", len(pos))
print("Part 2:", sum(loops_with_wall(p) for p in pos if p != guard))
