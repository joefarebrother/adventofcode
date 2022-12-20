from utils import *

inp = ints(inp_readlines())

xs = list(enumerate(inp))


def move(xs: list, idx):
    nidx = next(i for i, (j, x) in enumerate(xs) if j == idx)
    (j, v) = xs[nidx]
    assert j == idx
    xs = xs[:nidx] + xs[nidx+1:]
    nidx = (nidx + v) % len(xs)
    xs = xs[:nidx] + [(j, v)] + xs[nidx:]
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

# sol_simple:
# real    0m10.871s
# user    0m10.793s
# sys     0m0.063s

# sol:
# real    0m48.437s
# user    0m48.366s
# sys     0m0.038s

# lol, really overengineered it this time...
