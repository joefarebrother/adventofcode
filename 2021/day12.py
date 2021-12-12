from utils import *

inp = readlines(12)

gr = defaultdict(list)

for line in inp:
    a, b = line.split("-")
    gr[a].append(b)
    gr[b].append(a)


def paths(pt, part, visited=None):
    if pt == "end":
        return 1
    if visited == None:
        visited = [pt]
    c = 0
    for b in gr[pt]:
        if b not in visited or b.isupper() or (part == 2 and b not in ["start", "end"] and is_uniq(filter(lambda x: x.islower(), visited))):
            c += paths(b, part, visited+[b])
    return c


print("Part 1:", paths("start", 1))
print("Part 2:", paths("start", 2))
