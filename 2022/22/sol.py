from utils import *

gr, path = inp_groups()
gr = Grid(gr, y_is_down=True, default=' ')

path = re.findall(r'\d+|[LR]', path[0])
path = [mint(x, x) for x in path]

Dirs.flipy()

dr = Dirs.R
for x in range(gr.width()):
    if gr[x, 0] == '.':
        opos = IVec2(x, 0)
        break

pos = opos


def step():
    global pos
    npos = pos+dr
    if gr[npos] == ' ':
        npos = pos-dr
        while gr[npos] != ' ':
            npos -= dr
        npos += dr
    if gr[npos] == '.':
        pos = npos
        return True
    assert gr[npos] == '#', gr[npos]
    return False


for x in path:
    if isinstance(x, int):
        for _ in range(x):
            if not step():
                break
    else:
        dr *= Dirs['t'+x]

res = 1000*(pos.y+1) + 4*(pos.x+1) + [Dirs.R, Dirs.D, Dirs.L, Dirs.U].index(dr)
print("Part 1:", res)

edges1 = []
for p in gr:
    for d in neighbours(0):
        if gr[p] != ' ' and gr[p+d] == ' ':
            np = p
            while gr[np] != ' ' and gr[np+d] == ' ':
                np += d*Dirs.tR
            np1 = np-d*Dirs.tR
            np = p
            while gr[np] != ' ' and gr[np+d] == ' ':
                np += d*Dirs.tL
            np2 = np-d*Dirs.tL
            r = Rectangle(np1, np2)
            if r not in edges1:
                edges1.append(r)

size = min(max(r.width(), r.height()) for r in edges1)

edges2 = []
for e in edges1:
    l = list(e)
    for c in chunks(l, size):
        edges2.append(Rectangle(*c))

for e in edges2:
    print(e)
assert len(edges2) == 14, len(edges2)

# hard-coded
edge_pairings = {0: 6, 8: 9, 3: 10, 5: 1, 7: 12, 2: 11, 4: 13} if is_ex else {1: 10, 5: 6, 11: 12, 4: 7, 3: 13, 0: 8, 2: 9}
edge_flips = [8, 3, 5, 7, 2, 4] if is_ex else [4, 0]

edge_pairings = edge_pairings | inv_mapping(edge_pairings)


def step2():
    global pos, dr
    npos = pos+dr
    ndr = dr
    if gr[npos] == ' ':
        ei = only(i for i, e in enumerate(edges2) if pos in e and (pos+dr*Dirs.tL in e or pos+dr*Dirs.tR in e))
        oei = edge_pairings[ei]
        flip = (ei in edge_flips or oei in edge_flips)
        e = list(edges2[ei])
        oe = list(edges2[oei])
        if flip:
            oe = oe[::-1]
        npos = oe[e.index(pos)]
        ndr = only(d for d in neighbours(0) if gr[npos-d] == ' ' and (npos+d*Dirs.tL in oe or npos+d*Dirs.tR in oe))
        print(pos, dr, ei, oei, flip, npos, ndr)
    if gr[npos] == '.':
        pos = npos
        dr = ndr
        return True
    assert gr[npos] == '#', gr[npos]
    return False


pos = opos
dr = Dirs.R

dgr = Grid(gr)

for x in path:
    if isinstance(x, int):
        for _ in range(x):
            dgr[pos] = {Dirs.R: '>', Dirs.L: '<', Dirs.U: '^', Dirs.D: 'v'}[dr]
            if not step2():
                break
    else:
        dr *= Dirs['t'+x]

# dgr.draw()
print(pos, dr)

res = 1000*(pos.y+1) + 4*(pos.x+1) + [Dirs.R, Dirs.D, Dirs.L, Dirs.U].index(dr)
print("Part 2:", res)
