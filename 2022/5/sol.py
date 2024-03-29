from utils import *

crates_raw, instrs = inp_groups()

crates = defaultdict(list)
for line in crates_raw[::-1][1:]:
    row = line[1::4]
    for i, ch in enumerate(row):
        if ch != " ":
            crates[i+1].append(ch)


def do_part(crates, part):
    crates = deepcopy(crates)
    for instr in instrs:
        amt, src, dest = ints_in(instr)
        new, moved = crates[src][:-amt], crates[src][-amt:]
        crates[src] = new
        crates[dest] += (moved[::-1] if part == 1 else moved)
    return "".join(crates[i][-1] for i in irange(len(crates)))


print("Part 1:", do_part(crates, 1))
print("Part 2:", do_part(crates, 2))
