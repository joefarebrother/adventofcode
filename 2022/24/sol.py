from utils import *

gr = Grid(0, y_is_down=True)

internal_width = gr.width()-2
internal_height = gr.height()-2
period = math.lcm(internal_height, internal_width)

Dirs.flipy()

blizzards = []
for p, v in gr.items():
    if v in "^v<>":
        blizzards.append((p, Dirs[v]))


blizz_steps = set()

for opb, d in blizzards:
    for i in range(period):
        pb = opb+d*i
        pb = IVec2(mod_inc(pb.x, internal_width), mod_inc(pb.y, internal_height))
        blizz_steps.add((pb, i))

startp = IVec2(1, 0)
start = startp, 0
endp = IVec2(internal_width, gr.height()-1)
print(endp)

steps = [0]


def adj(pi):
    p, i = pi
    ni = (i+1) % period
    # if steps[0] % 100 == 0:
    #     print(steps, len(grph.pqueue), grph.dists[pi], grph.dists[pi]+h(pi))
    # steps[0] += 1
    for np in neighbours(p)+[p]:
        if np in gr and gr[np] != '#' and not (np, ni) in blizz_steps:
            yield np, ni


def h(pi):
    return man_dist(pi[0], endp)


grph = FGraph(adj=adj).dist1()
node, dist = grph.astar(start, h=h).find(lambda pi: pi[0] == endp)

# print(list(grph.get_path(node)))

print("Part 1:", dist)

start2 = startp, 0, 0


def adj2(pis):
    p, i, s = pis
    ni = (i+1) % period
    # if steps[0] % 100 == 0:
    #     print(steps, len(grph2.pqueue), grph2.dists[pis], grph2.dists[pis]+h2(pis))
    # steps[0] += 1
    for np in neighbours(p)+[p]:
        if np in gr and gr[np] != '#' and not (np, ni) in blizz_steps:
            ns = s
            if np == endp and s == 0:
                ns = 1
            if np == startp and s == 1:
                ns = 2
            yield np, ni, ns


def h2(pis):
    p, _i, s = pis
    goal = [endp, startp, endp][s]
    return man_dist(p, goal)+(2-s)*man_dist(startp-endp)


grph2 = FGraph(adj=adj2).dist1()
node, dist = grph2.astar(start2, h=h2).find(lambda pi: pi[0] == endp and pi[2] == 2)

print("Part 2:", dist)
