from utils import *

grid = Grid("input18")

key_pos = {k: p for p, k in grid.items() if k.islower()}

for p in grid:
    if grid[p] == '@':
        start_pos = p


def get_dists_from(spos):
    """
    Compute the distance to each key from spos and the doors that must be passed though.
    Relies on the fact that there's no way to go "around" any doors without its key in the input.
    """
    res = {}

    def adj(p_):
        p, doors = p_
        c = grid[p]
        if c.isupper():
            doors |= {c.lower()}
        if c != '#':
            return [(q, doors) for q in neighbours(p)]
    gr = FGraph(adj, key=lambda p_: p_[0])
    for ((p, doors), dist) in gr.BFS((spos, frozenset())):
        c = grid[p]
        if c.islower():
            res[c] = (doors, dist)
    return res


def get_key_dists():
    """Computes the distances and doors required between each pair of keys"""
    return {k: get_dists_from(p) for k, p in key_pos.items()}


key_dists = get_key_dists()
key_dists['@'] = get_dists_from(start_pos)


def adj1(p_):
    """
    Adjancency function for the graph whose nodes encode which keys have been collected so far + the most recent one
    """
    p, ks = p_
    # print(astar.dist, len(astar.pqueue), p)
    return {(q, ks | {q}): dist for (q, (doors, dist)) in key_dists[p].items() if doors <= ks and q not in ks}


def end_cond(p):
    return len(p[1]) == len(key_pos)


@cache
def minpath(p, adj):
    if end_cond(p):
        return 0
    return min(d+minpath(p, adj) for p, d in adj(p).items())


# part 1:
print(minpath(('@', frozenset()), adj1))

starts = []
for x in range(-1, 2):
    for y in range(-1, 2):
        pos = x+y*1j
        if x*y == 0:
            grid[start_pos + pos] = '#'
        else:
            grid[start_pos + pos] = '@'
            starts += [start_pos + pos]
starts = tuple(starts)

key_dists = get_key_dists()
for i, p in enumerate(starts):
    key_dists[i] = get_dists_from(p)


def adj2(p_):
    """
    Adjecency function for the graph whose nodes include the set of keys collected so far
    and the most recently collected ones for each of the 4 bots
    """
    ps, ks = p_

    # print(len(ks), gr.dists[p_], len(gr.pqueue))

    res = []
    for i, p in enumerate(ps):
        moves = [((q, ks | {q}), dist) for (q, (doors, dist))
                 in key_dists[p].items() if doors <= ks and q not in ks]
        res += [((modify_idx(ps, i, q), nks), dist)
                for ((q, nks), dist) in moves]

    return {n: d for (n, d) in res}


# min_dist = min([key_dists[p][q][1] for p in key_dists for q in key_dists[p]])

# gr = FGraph(adj2)
start = ((0, 1, 2, 3), frozenset())
# for ((_, ks), d) in gr.astar_gen(start, h=lambda p_: min_dist *
#                                  (len(key_pos) - len(p_[1]))):
#     print(len(ks), d, len(gr.pqueue))
#     if len(ks) == len(key_pos):
#         print(d)
#         exit()


print(minpath(start, adj2))
