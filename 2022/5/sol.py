from utils import *

crates_raw, instrs = inp_groups()

crates = [[] for _ in range(max(ints_in(crates_raw[-1]))+1)]
for line in crates_raw[::-1][1:]:
    row = line[1::4]
    for i, ch in enumerate(row):
        if ch != " ":
            crates[i+1].append(ch)

for instr in instrs:
    amt, src, dest = ints_in(instr)
    #print(amt, src, dest, crates)
    # for _ in range(amt):
    #    crates[dest].append(crates[src].pop())
    new, moved = crates[src][:-amt], crates[src][-amt:]
    print(amt, src, dest, crates[src], moved, new)
    crates[src] = new
    crates[dest] += moved

print("Part 2:", "".join(crate[-1] for crate in crates[1:]))
