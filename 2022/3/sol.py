from utils import *

rucks = []
for i, line in enumerate(inp_readlines()):
    half = len(line)//2
    c1, c2 = line[:half], line[half:]
    rucks.append((set(c1), set(c2), i//3))


def pri(s: str):
    if s.isupper():
        return ord(s)-ord("A")+27
    else:
        return ord(s)-ord("a")+1


tot = 0
for (c1, c2, i) in rucks:
    tot += sum(pri(s) for s in c1 & c2)

print("Part 1:", tot)

rucks_by_id = defaultdict(list)
for (c1, c2, i) in rucks:
    rucks_by_id[i].append(c1 | c2)

tot = 0
for _, cs in rucks_by_id.items():
    c1, c2, c3 = cs
    c = c1 & c2 & c3
    assert len(c) == 1
    tot += pri(next(iter(c)))

print("Part 2:", tot)
