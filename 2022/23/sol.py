from utils import *

gr = Grid(0, y_is_down=False)
gr = set(p for p, v in gr.items() if v == '#')


def step(gr, i):
    dirs = [Dirs.N, Dirs.S, Dirs.W, Dirs.E]
    for _ in range(i):
        dirs.append(dirs.pop(0))
    nxt = defaultdict(list)
    stay = set()
    for p in gr:
        for dp in neighbours8(p):
            if dp in gr:
                break
        else:
            stay.add(p)
            continue
        for d in dirs:
            for dd in [d, d+d*Dirs.tL, d+d*Dirs.tR]:
                if p+dd in gr:
                    break
            else:
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
    dgr = Grid(y_is_down=False)
    for p in gr:
        dgr[p] = '#'
    dgr.draw()


print("Init:")
draw(gr)

for i in range(10):
    gr = step(gr, i)
    print("Round", i)
    draw(gr)

bb = bounding_box(gr)
area = len(bb)


print("Part 1:", area - len(gr))

i += 1
while True:
    ngr = step(gr, i)
    if ngr == gr:
        print("Part 2:", i+1)
        exit()
    print("Round", i)
    # draw(gr)
    gr = ngr
    i += 1
