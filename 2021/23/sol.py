from utils import *

g = Grid(23)

extra = Grid("""  #D#C#B#A#
  #D#B#A#C#""".splitlines())

ng = Grid(y_is_down=True)
for p in g:
    x, y = pos_as(tuple, p)
    if y < 3:
        ng[p] = g[p]
    else:
        if y < 5:
            ng[p] = extra[x, y-3]
        ng[x, y+2] = g[p]


g = ng
g.draw()

rooms = {l: [x+y*1j for y in [2, 3, 4, 5]]
         for x in [3, 5, 7, 9] for l in ["___A_B_C_D"[x]]}
hallway = [x+1j for x in irange(1, g.width()-2) if x not in [3, 5, 7, 9]]
energy = {l: 10**i for i, l in enumerate("ABCD")}

occupied = {p: l for p, l in g.items() if l in "ABCD"}


def path(occ, start, end):
    ps = ({start.real+y*1j for y in irange(1, int(start.imag))} | {end.real+y*1j for y in irange(
        1, int(end.imag))} | {x+1j for x in irange(*ints(bounds((start.real, end.real))))}) - {start}
    if all(p not in occ for p in ps):
        return len(ps)


def room_free(occ, l):
    return all(p not in occ or occ[p] == l for p in rooms[l])


def is_home(occ, p):
    if p not in occ:
        return False
    l = occ[p]
    ps = rooms[l]
    return p in ps and all(q in occ and occ[q] == l for q in ps if q.imag > p.imag)


def moves(occ):
    res = []
    # hallway to room
    for h in hallway:
        if h in occ:
            l = occ[h]
            ps = rooms[l]
            if room_free(occ, l):
                i = -1
                while ps[i] in occ:
                    i -= 1
                p = ps[i]
                d = path(occ, h, p)
                if d:
                    res.append((h, p, d*energy[l]))
    # room to hallway
    for l, ps in rooms.items():
        for p in ps:
            if p in occ:
                if not is_home(occ, p):
                    for h in hallway:
                        d = path(occ, p, h)
                        if d:
                            res.append((p, h, d*energy[occ[p]]))
    return res


def adj(occ):
    occ = dict(occ)
    res = {}
    for start, end, d in moves(occ):
        nocc = dict(occ)
        del nocc[start]
        nocc[end] = occ[start]
        nocc = frozenset((p, l) for p, l in nocc.items() if l != None)
        res[nocc] = d
    # if gr:
    #     print(len(gr.pqueue))
    return res


def end_cond(occ):
    for p, l in occ:
        if p not in rooms[l]:
            return False
    return True


def print_state(occ):
    occ = dict(occ)
    ng = Grid(g)
    for p in ng:
        if ng[p] in "ABCD":
            ng[p] = "."
    for p in occ:
        ng[p] = occ[p]
    ng.draw()


gr = None

# print_state(occupied)
# for m in adj(occupied):
#     print_state(m)


gr = FGraph(adj)


def room_dist(a, b):
    return a.imag+b.imag-2+(abs(a.real-b.real) or 2)


def target(occ, l):
    for p in rooms[l][::-1]:
        if p not in occ or occ[p] != l:
            return p


def h(occ):
    occ = dict(occ)
    res = 0
    c = Counter()
    for p, l in occ.items():
        if is_home(occ, p):
            continue
        res += energy[l] * (room_dist(p, target(occ, l)) - c[l])
        c[l] += 1

    return res


end, d = gr.astar(frozenset(occupied.items()), end_cond, h)
# end, d = gr.DAG_search(frozenset(occupied.items()), end_cond)
print("====")
for occ in gr.get_path(end):
    print_state(occ)
    # print(gr.dists[occ])
print(d)


# DAG search:
# real    0m41.489s
# user    0m41.338s
# sys     0m0.137s

# Dijkstra:
# real    0m41.489s
# user    0m41.338s
# sys     0m0.137s

# A*:
# real    0m29.334s
# user    0m29.219s
# sys     0m0.113s
