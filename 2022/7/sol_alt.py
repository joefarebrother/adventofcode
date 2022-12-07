from utils import *

sizes = Counter()
path = ["/"]

# This alternate solution exploits the fact that we never care about the name of anything, and we never ls the same directory twice.

for cmd in inp_readlines():
    if cmd.startswith("$ cd"):
        f = cmd.split()[-1]
        if f == "/":
            path = ["/"]
        elif f == "..":
            path.pop()
        else:
            path.append(f)
    elif cmd.startswith("$ ls"):
        pass
    else:
        size, _name = cmd.split()
        if size != "dir":
            for i in irange(len(path)):
                sizes[tuple(path[:i])] += int(size)

free = 70000000 - sizes[("/",)]
print("Part 1:", sum(sz for sz in sizes.values() if sz <= 100000))
print("Part 2:", min(sz for sz in sizes.values() if sz >= 30000000 - free))
