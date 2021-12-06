import sys
import re
from collections import defaultdict

inp = list(open(sys.argv[1]))
inp = [int(x) for x in inp[0].split()]

nodes = []


class Node:
    def __init__(self, xs):
        self.size = xs.pop(0)
        self.meta_size = xs.pop(0)
        self.nodes = []
        self.meta = []
        for i in range(self.size):
            self.nodes.append(Node(xs))
        for i in range(self.meta_size):
            self.meta.append(xs.pop(0))

        nodes.append(self)

    def value(self):
        if not self.nodes:
            return sum(self.meta)
        s = 0
        for n in self.meta:
            if n <= len(self.nodes) and n > 0:
                s += self.nodes[n-1].value()
        return s


root = Node(inp)
print(sum(sum(m for m in n.meta) for n in nodes))
print(root.value())
