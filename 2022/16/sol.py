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


@cache
def pressure(time, v, open, part2):
    best = pressure(26, "AA", open, False) if part2 else 0
    if time <= 1:
        return best
    for v2, d in dists[v].items():
        fr = valves[v2][0]
        ntime = time-d-1
        if ntime >= 0 and v2 in bits and not bits[v2] & open:
            best = max(best, fr*ntime + pressure(ntime, v2, open | bits[v2], part2))
    return best


print("Part 1:", pressure(30, "AA", 0, False))

print("Part 2:", pressure(26, "AA", 0, True))
