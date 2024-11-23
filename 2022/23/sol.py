from utils import *

gr = Grid(0)
gr = set(p for p, v in gr.items() if v == '#')


def step(gr, i):
    dirs = [Dirs.N, Dirs.S, Dirs.W, Dirs.E]
    for _ in range((i-1) % 4):
        dirs.append(dirs.pop(0))
    nxt = defaultdict(list)
    stay = set()
    for p in gr:
        if all(np not in gr for np in neighbours8(p)):
            stay.add(p)
            continue
        for d in dirs:
            if all(p+d+d*dd not in gr for dd in [0, Dirs.tL, Dirs.tR]):
                nxt[p+d].append(p)
                break
        else:
            stay.add(p)
    nxtgr = stay
    for n, ps in nxt.items():
        if len(ps) == 1:
            nxtgr.add(n)
        else:
            nxtgr |= set(ps)
    assert len(nxtgr) == len(gr)
    return nxtgr


def draw(gr):
    dgr = Grid()
    for p in gr:
        dgr[p] = '#'
    dgr.draw()


print("Init:")
draw(gr)

i = 1
while True:
    ngr = step(gr, i)
    if i == 10:
        bb = bounding_box(ngr)
        area = len(bb)
        print("Part 1:", area - len(ngr))
    if ngr == gr:
        print("Part 2:", i)
        exit()
    print("Round", i)
    # draw(gr)
    gr = ngr
    i += 1
