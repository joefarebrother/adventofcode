from utils2020 import *
from collections import deque

grid = Grid("input20")


def find_portal(lab):
    res = []
    for (p, c) in grid.items():
        if c == lab[0]:
            if p+1 in grid and grid[p+1] == lab[1]:
                if p+2 in grid and grid[p+2] == '.':
                    res += [(p+2, p-1)]
                elif p-1 in grid and grid[p-1] == '.':
                    res += [(p-1, p+2)]
            elif p+1j in grid and grid[p+1j] == lab[1]:
                if p+2j in grid and grid[p+2j] == '.':
                    res += [(p+2j, p-1j)]
                elif p-1j in grid and grid[p-1j] == '.':
                    res += [(p-1j, p+2j)]

    if len(res) == 2:
        if res[0][1] not in grid:  # ensure outer comes first
            res = res[::-1]

    return [p for (p, _) in res]


portals = {}
for (p, c) in grid.items():
    if c.isupper():
        for p2 in [p+1j**dir for dir in range(4)]:
            if p2 in grid:
                c2 = grid[p2]
                if c2.isupper():
                    port = find_portal(c+c2)
                    if len(port) == 2:
                        portals[port[0]] = (port[1], 1, c+c2)
                        portals[port[1]] = (port[0], -1, c+c2)

print(portals)
print(len(portals.keys()))

start = find_portal("AA")[0]
end = find_portal("ZZ")[0]


def adj1(p):
    c = grid[p]
    if c == '.':
        res = neighbours(p)
        if p in portals:
            (np, _, _) = portals[p]
            res += [np]
        return res


print(BFS(start, adj1, end))


def adj2(p_):
    p, l = p_
    c = grid[p]
    if l >= 0 and c == '.':
        res = [(q, l) for q in neighbours(p)]
        if p in portals:
            (np, dl, lab) = portals[p]
            res += [(np, l+dl)]
            #print(l+dl, d, len(queue), lab)
        return res


print(BFS((start, 0), adj2, (end, 0)))
