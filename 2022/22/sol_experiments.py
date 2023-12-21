from utils import *

gr, path = inp_groups()
gr = Grid(gr, y_is_down=True, default=' ')

path = re.findall(r'\d+|[LR]', path[0])
path = [mint(x, x) for x in path]

Dirs.flipy()

dr = Dirs.R
for x in range(gr.width):
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

identified = {}


def identify(pd1, pd2):
    p1, d1 = pd1
    p2, d2 = pd2
    assert gr[p1] != ' ' and gr[p1+d1] == ' ' and gr[p2] != ' ' and gr[p2+d2] == ' '
    identified[p1+d1, d1] = (p2, -d2)
    identified[p2+d2, d2] = (p1, -d1)


start = opos, Dirs.R
pos = opos
dr = Dirs.R
# walk the perimeter
perim_with_angles = []
while (pos, dr) != start or not perim_with_angles:
    # invariant: gr[pos+dr*Dirs.tl] == ' '
    match (gr[pos+dr] == ' ', gr[pos+dr+dr*Dirs.tL] == ' '):
        case (False, True):
            #
            #  ...>...
            #  .......
            perim_with_angles.append((pos, dr, 2))
            pos += dr
        case (False, False):
            #      ...
            #  ...>...
            #  .......
            perim_with_angles.append((pos, dr, 3))
            pos += dr+dr*Dirs.tL
            dr *= Dirs.tL
        case (True, _):
            #
            #  ...>
            #  ....
            perim_with_angles.append((pos, dr, 1))
            dr *= Dirs.tR

#sz = 4 if is_ex else 50
sz = 1
perim_with_angles = mapl(lambda p: (p[0], p[1]*Dirs.tL, p[2]), perim_with_angles)
#assert len(perim_with_angles) == sz*14

edges_ = chunks(perim_with_angles, sz)
edges = []
for e in edges_:
    assert all(p[2] == 2 for p in e[:-1])
    edges.append([[p[:2] for p in e], e[-1][2]])


while edges:
    print(l := [e[1] for e in edges], sum(l))
    # maxl = max(l)
    # assert maxl >= 3
    # assert l.count(3) >= 2  # Toby proved this
    cands = []
    for i in range(len(edges)):
        e1 = edges[i]
        e2 = edges[(i+1) % len(edges)]
        if e1[1] >= 3:
            cands.append((i, edges[i-1][1]+e2[1]))
    cands = sorted(cands, key=lambda c: c[1])
    edges_ = []
    for i in range(len(edges)):
        e1 = edges[i]
        e2 = edges[(i+1) % len(edges)]
        if i == cands[0][0]:
            for pd1, pd2 in zip(e1[0], reversed(e2[0]), strict=True):
                identify(pd1, pd2)
            edges[i-1][1] = (edges[i-1][1]+e2[1])
            # assert edges[i-1][1] in [1, 2, 3, 4] + [6]*(len(edges) == 2), (i, len(edges), edges[i-1][1], e2[1])
            edges_ += edges[i+2:]
            if i == len(edges)-1:
                edges_.pop(0)
            break
        else:
            edges_.append(edges[i])
    else:
        raise Exception("???")

    edges = edges_


pos = opos
dr = Dirs.R


def step2():
    global pos, dr
    npos = pos+dr
    ndr = dr
    if gr[npos] == ' ':
        npos, ndr = identified[npos, dr]
    if gr[npos] == '.':
        pos = npos
        dr = ndr
        return True
    assert gr[npos] == '#', gr[npos]
    return False


for x in path:
    if isinstance(x, int):
        for _ in range(x):
            if not step2():
                break
    else:
        dr *= Dirs['t'+x]

# dgr.draw()
print(pos, dr)

res = 1000*(pos.y+1) + 4*(pos.x+1) + [Dirs.R, Dirs.D, Dirs.L, Dirs.U].index(dr)
print("Part 2:", res)
