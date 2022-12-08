from utils import *

inp = Grid(0, ints=True)


def vis_in_dir(p, d):
    """
    Returns n, vis where n is the number of trees visible in direction d from point p, 
    and vis is True if p is visible from the edge.
    """
    p0 = p
    i = 0
    while p in inp and p+d in inp:
        p += d
        i += 1
        if inp[p] >= inp[p0]:
            return i, False
    return i, True


def vis(p):
    return any(vis_in_dir(p, d)[1] for d in neighbours(0))


print("Part 1:", sum(vis(p) for p in inp))


def score(p):
    return math.prod(vis_in_dir(p, d)[0] for d in neighbours(0))


print("Part 2:", max(score(p) for p in inp))
