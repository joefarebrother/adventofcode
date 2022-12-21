from utils import *

inp = ints(inp_readlines())


class SkipNode:
    def __init__(self, val, maxlinks):
        self.val = val
        self.links = []
        self.backlinks = []
        self.maxlinks = maxlinks

        # invariants:
        # maxlinks is constant for each node in the list
        # 1 <= len(self.links) = len(self.backlinks) <= maxlinks
        # there is a node with len(self.links) == maxlinks()
        # if b.links[j] = (lf,f), then len(f.backlinks) >= j+1 and f.backlinks[j] = (lf,b)
        # self.links[0][0] == 1
        # the distances are consistent

    def _init_link(self, other, lf):
        self.links.append((lf, other))
        other.backlinks.append((lf, self))

    def get(self, n):
        assert n >= 0
        x = self
        while n:
            for lf, f in reversed(x.links):
                if lf <= n:
                    n -= lf
                    x = f
                    break
        return x

    def getfs(self):
        res = []
        lf, f = 0, self
        for j in range(self.maxlinks):
            if j < len(self.links):
                lf, f = self.links[j]
                res.append((lf, f))
            else:
                while j >= len(f.links):
                    lff, f = f.links[-1]
                    lf += lff
                res.append((lf, f))
        return res

    def shift(self, n):
        if n == 0:
            return
        after = self.get(n)

        # remove self
        fs = self.getfs()
        for j in range(self.maxlinks):
            if j < len(self.links):
                lf, f = self.links[j]
                lb, b = self.backlinks[j]
                lbf = lf+lb-1,
                f.backlinks[j] = (lbf, b)
                b.links[j] = (lbf, f)
            else:
                lf, f = fs[j]
                lbf, b = f.backlinks[j]
                f.backlinks[j] = (lbf-1, b)
                b.links[j] = (lbf-1, f)

        # insert self
        fs = after.getfs()
        for j in range(self.maxlinks):
            lf, f = fs[j]
            lbf, b = f.backlinks[j]
            if j < len(self.links):
                self.links[j] = (lf, f)
                f.backlinks[j] = (lf, self)
                lb = lbf-lf+1
                self.backlinks[j] = (lb, b)
                b.links[j] = (lb, self)
            else:
                f.backlinks[j] = (lbf+1, b)
                b.links[j] = (lbf+1, f)


def build_skiplist(xs):
    maxlinks = len(bin(len(xs)))-2
    zidx = xs.index(0)
    nodes = [SkipNode(x, maxlinks) for x in xs]
    nodes2 = nodes[zidx:] + nodes[:zidx]

    for j in range(maxlinks):
        for h in range(0, len(nodes), 2**j):
            dst = 2**j
            if h+dst >= len(nodes):
                dst = len(nodes)-h
            x = nodes2[h]
            y = nodes2[(h+dst) % len(nodes)]
            x._init_link(y, dst)  # pylint:disable=protected-access

    assert len(nodes2[0].links) == maxlinks

    return nodes


def debug(nodes):
    for i in range(len(nodes)):
        n = nodes[0].get(i)
        print(f'{n.val:11}', end=", ")
    print()
    for j in range(nodes[0].maxlinks):
        for i in range(len(nodes)):
            n = nodes[0].get(i)
            if j >= len(n.links):
                print(" "*11, end="  ")
            else:
                lf, f = n.links[j]
                lb, b = n.backlinks[j]
                print(f'{lb:2} {b.val:2} {f.val:2} {lf:2}', end=", ")
        print()
    print("\n\n\n")


def run(xs: list, mixes):
    zidx = xs.index(0)
    nodes = build_skiplist(xs)

    for _ in range(mixes):
        for n in nodes:
            n.shift(n.val % (len(nodes)-1))

            # debug(nodes)

    return sum(nodes[zidx].get(n*1000).val for n in irange(1, 3))


print("Part 1:", run(inp, 1))
print("Part 2:", run([x*811589153 for x in inp], 10))

# https://www.reddit.com/r/adventofcode/comments/zqwwjy/2022_day_20_part_3/ - custom part 3

if is_ex:  # can't run the part 3 on my real input
    xs = []
    for i in irange(10000):
        for x in inp:
            if x != 0 or i == 1:
                xs.append(x*i*811589153)

    print("Part 3:", run(xs, 10))
