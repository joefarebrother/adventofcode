from utils import *

inp = inp_readall().strip()

files = []
for (i,s) in enumerate(inp):
    files += [i//2 if i&1==0 else None]*int(s)
ofiles = list(files) 

lo = 0
hi = len(files)-1 

while lo < hi:
    if files[lo] is not None:
        lo+=1
        continue 
    if files[hi] is None:
        hi -= 1
        continue 
    files[lo]=files[hi]
    files[hi]=None 
    lo+=1 
    hi-=1 

print("Part 1:", sum(off*id for off,id in enumerate(files) if id is not None))

free = defaultdict(list, {-1:[math.inf]}) # for each size, track offset of free blocks in a min-heap
files = []
raw_files = []
off = 0
for (i,s) in enumerate(inp):
    s = int(s)
    if i&1 and s:
        free[s].append(off)
    else:
        files.append((i//2, s, off))
    off += s

raw_files = [None]*off

import heapq
for id,s,off in files[::-1]:
    fs= min([fs for fs in free if fs >= s and free[fs]], key=lambda fs:free[fs][0], default=-1)
    foff = free[fs][0]
    if foff > off:
        raw_files[off:off+s] = [id]*s
    else:
        heapq.heappop(free[fs])
        raw_files[foff:foff+s] = [id]*s
        if fs > s:
            heapq.heappush(free[fs-s], foff+s)

print("Part 2:", sum(off*id for off,id in enumerate(raw_files) if id is not None))










