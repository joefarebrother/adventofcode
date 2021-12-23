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
hallway = [x+1j for x in irange(1, g.width()-1) if x not in [3, 5, 7, 9]]
energy = {l: 10**i for i, l in enumerate("ABCD")}

occupied = {p: l for p, l in g.items() if l in "ABCD"}
printx(occupied)


def path(occ, start, end):
    def empty(p):
        return g[p] != "#" and p not in occ
    found, d = FGraph(
        lambda p: [n for n in neighbours(p) if empty(n)]).BFS(start, end)
    if found:
        return d


def room_free(occ, l):
    return all(p not in occ or occ[p] == l for p in rooms[l])


def moves(occ):
    res = []
    # hallway or room to room
    for h, l in occ.items():
        ps = rooms[l]
        if room_free(occ, l) and h not in ps:
            i = -1
            while ps[i] in occ:
                i -= 1
            p = ps[i]
            d = path(occ, h, p)
            if d:
                res.append((h, p, d*energy[l]))
    # room to hallway
    for l, ps in rooms.items():
        if not all(p in occ and occ[p] == l for p in ps):
            for p in ps:
                if p in occ:
                    for h in hallway:
                        d = path(occ, p, h)
                        if d:
                            res.append((p, h, d*energy[occ[p]]))
    # hallway to hallway # this is incorrect
    # for h1, h2 in it.permutations(hallway, 2):
    #     if h1 in occ and not h2 in occ and room_free(occ, occ[h1]):
    #         d = path(occ, h1, h2)
    #         if d:
    #             res.append((h1, h2, d*energy[occ[h1]]))
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

print_state(occupied)
for m in adj(occupied):
    print_state(m)


gr = FGraph(adj)


def room_dist(a, b):
    return a.imag+b.imag-2+min(abs(a.real-b.real), 2)


def target(occ, l):
    for p in rooms[l][::-1]:
        if p not in occ or occ[p] != l:
            return p


def h(occ):
    occ = dict(occ)
    res = 0
    for p, l in occ.items():
        if p in rooms[l]:
            ps = rooms[l]
            if all(q in occ and occ[q] == l for q in ps if q.imag > p.imag):
                continue
        res += energy[l] * room_dist(p, target(occ, l))

    return res


end, d = gr.astar(frozenset(occupied.items()), end_cond, h)
print("====")
for occ in gr.get_path(end):
    print_state(occ)
    print(gr.dists[occ])
print(d)
