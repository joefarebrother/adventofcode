from utils import *

inp = ints(inp_readlines())

xs = list(enumerate(inp))


def move(xs: list, idx):
    nidx = next(i for i, (j, x) in enumerate(xs) if j == idx)
    (j, v) = xs.pop(nidx)
    assert j == idx
    nidx = (nidx + v) % len(xs)
    xs.insert(nidx, (j, v))
    return xs


def mix(xs):
    for i in range(len(xs)):
        xs = move(xs, i)
    return xs


def res(xs):
    zidx = next(i for i, (j, x) in enumerate(xs) if x == 0)
    idxs = [(zidx+k*1000) % len(xs) for k in irange(3)]
    return sum(xs[idx][1] for idx in idxs)


print("Part 1:", res(mix(xs)))

xs = [(i, 811589153*x)for i, x in enumerate(inp)]

for _ in range(10):
    xs = mix(xs)

print("Part 2:", res(xs))
