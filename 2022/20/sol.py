from utils import *

inp = ints(inp_readlines())
print(len(set(inp)), len(inp))


class Node:
    def __init__(self, val):
        self.next = None
        self.prev = None
        self.val = val

    def unlink(self):
        pr = self.prev
        nx = self.next
        assert pr.next == self and nx.prev == self
        pr.next = nx
        nx.prev = pr
        self.next = None
        self.prev = None

    def link(self, pr, nx):
        self.unlink()
        assert pr.next == nx and nx.prev == pr
        self.next = nx
        nx.prev = self
        self.prev = pr
        pr.next = self

    def move_forward(self):
        self.link(self.next, self.next.next)

    def move_backward(self):
        self.link(self.prev.prev, self.prev)

    def move(self):
        if self.val < 0:
            for _ in range(-self.val % (len(nodes)-1)):
                self.move_backward()
        else:
            for _ in range(self.val % (len(nodes)-1)):
                self.move_forward()

    def get(self, n):
        x = self
        for _ in range(n):
            x = x.next
        return x


nodes = [Node(x) for x in inp]
zero = only(n for n in nodes if n.val == 0)

for x, y in windows(nodes+[nodes[0]], 2):
    x.next = y
    y.prev = x


def mix():
    for n in nodes:
        n.move()


mix()

res = sum(zero.get(i*1000).val for i in range(4))
print("Part 1:", res)

for x, y in windows(nodes+[nodes[0]], 2):
    x.next = y
    y.prev = x

for n in nodes:
    n.val *= 811589153

for _ in range(10):
    mix()

res = sum(zero.get(i*1000).val for i in range(4))
print("Part 2:", res)
