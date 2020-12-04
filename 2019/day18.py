from utils2020 import *

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
        if c.islower():
            res[c] = doors, BFS.dist
        if c != '#':
            return [(q, doors) for q in neighbours(p)]
    BFS((spos, frozenset()), adj, key=lambda p_: p_[0])
    return res


def get_key_dists():
    """Computes the distances and doors required between each pair of keys"""
    return {k: get_dists_from(p) for k, p in key_pos.items()}


key_dists = get_key_dists()
key_dists['@'] = get_dists_from(start_pos)

'''
def adj1(p_):
  p, ks = p_
  c = grid[p]

  nks = ks
  if c.islower():
    nks = nks | {c}
    print(len(nks), len(BFS.queue))

  if ok(c, nks):
    return [(q, nks) for q in neighbours(p)]
'''
# print(key_dists)


def adj1(p_):
    """ 
    Adjancency function for the graph whose nodes encode which keys have been collected so far + the most recent one
    """
    p, ks = p_
    #print(astar.dist, len(astar.pqueue), p)
    return [((q, ks | {q}), dist) for (q, (doors, dist)) in key_dists[p].items() if doors <= ks]


def end_cond(p):
    return len(p[1]) == len(key_pos)


def bits(s):
    res = 0
    for c in s:
        res |= (1 << (ord(c) - ord('a')))
    return res


# part 1:
print(dijkstra(('@', frozenset()), adj1, end_cond))


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

'''
def adj2(p_):
  ps, ks, cur = p_
  cs = [grid[p] for p in ps]
 
  nks = ks.union({k for k in cs if k.islower()})
  
  if len(nks) > len(ks):
    cur = None
    print(len(nks), len(BFS.queue), BFS.dist)
  if all([ok(c, nks) for c in cs]):
    moves = all_moves(ps) if cur == None else moves_for(ps,cur)
    return [(move, nks, rob) for (move, rob) in moves]
'''


def adj2(p_):
    """
    Adjecency function for the graph whose nodes include the set of keys collected so far 
    and the most recently collected ones for each of the 4 bots
    """
    ps, ks = p_

    print(len(ks), astar.dist, len(astar.pqueue))

    res = []
    for i, p in enumerate(ps):
        moves = [((q, ks | {q}), dist) for (q, (doors, dist))
                 in key_dists[p].items() if doors <= ks]
        res += [((ps[:i] + (q,) + ps[i+1:], nks), dist)
                for ((q, nks), dist) in moves]
    return res


min_dist = min([key_dists[p][q][1] for p in key_dists for q in key_dists[p]])

print(astar(((0, 1, 2, 3), frozenset()), adj2, end_cond,
            h=lambda p_: (len(key_pos) - len(p_[1]))*min_dist))
