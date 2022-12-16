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

fr_0 = frozenset(v for v, (fr, vs) in valves.items() if fr == 0)


@cache
def flowrate(time, v, open):
    if time == 0:
        return 0
    assert time > 0
    best = 0
    for v2, d in dists[v].items():
        fr = valves[v2][0]
        if time >= d+1 and v2 not in open:
            best = max(best, fr*(time-d-1)+flowrate(time-d-1, v2, open | {v2}))
    return best


print("Part 1:", flowrate(30, "AA", fr_0))


@cache
def flowrate2(time, v, open):
    if time == 0:
        return flowrate(26, "AA", open)
    assert time > 0
    best = flowrate(26, "AA", open)
    for v2, d in dists[v].items():
        fr = valves[v2][0]
        if time >= d+1 and v2 not in open:
            best = max(best, fr*(time-d-1)+flowrate2(time-d-1, v2, open | {v2}))
    return best


print("Part 2:", flowrate2(26, "AA", fr_0))
