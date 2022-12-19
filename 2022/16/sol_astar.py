from utils import *

valves = {}
for line in inp_readlines():
    v, fr, vs = match(r'Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.*)', line)
    vs = vs.split(", ")
    valves[v] = (fr, vs)

gr = FGraph(adj=lambda v: valves[v][1])

dists = defaultdict(dict)


for v in valves:
    for v2, d in gr.BFS(v):
        dists[v][v2] = d

bits = {}
for v, (fr, vs) in valves.items():
    if fr > 0:
        bits[v] = 1 << len(bits)

# pylint:disable=redefined-builtin


def pressure(time, part2):
    # best = pressure(26, "AA", open, False) if part2 else 0
    # if time <= 1:
    #     return best
    # for v2, d in dists[v].items():
    #     fr = valves[v2][0]
    #     ntime = time-d-1
    #     if ntime >= 0 and v2 in bits and not bits[v2] & open:
    #         best = max(best, fr*ntime + pressure(ntime, v2, open | bits[v2], part2))
    # return best
    def adj(node, _pr=True):
        time, v, open, ele = node
        # as noted in 2022/19, A* is correct even with negative weights provided the heuristic is consistent, and the heuristic at goal nodes is constant.
        # if _pr:
        #     print((time, v, f"{open:15b}", ele), gr.dists[node], h(node), gr.dists[node]+h(node))
        res = {}
        if ele:
            res[26, "AA", open, False] = 0
        for v2, d in dists[v].items():
            fr = valves[v2][0]
            ntime = time - (d+1)
            if ntime >= 0 and v2 in bits and not bits[v2] & open:
                res[ntime, v2, open | bits[v2], ele] = -fr*ntime
        return res

    def h(node):
        time, _v, open, ele = node
        if not adj(node, _pr=False):
            return 0
        remaining_fr = sum(valves[v2][0] for v2, b in bits.items() if not b & open)
        h = -remaining_fr*max(time-1, 25*ele, 0)
        return h

    gr = FGraph(adj)
    _node, dist = gr.astar((time, "AA", 0, part2), h).find(lambda n: not adj(n))
    # for nd in gr.get_path(_node):
    #     time, v, open, ele = nd
    #     print((time, v, f"{open:15b}", ele), gr.dists[nd], valves[v][0])
    return -dist


print("Part 1:", pressure(30, False))

print("Part 2:", pressure(26, True))

# sol_astar.py:
# real    1m56.886s
# user    1m56.151s
# sys     0m0.624s

# sol.py
# real    0m17.695s
# user    0m17.471s
# sys     0m0.192s

# so, A* does not seem worthwhile here. though it was good for day 19...
