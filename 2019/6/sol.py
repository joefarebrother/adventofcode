from utils import DGraph, inp_readlines
from collections import defaultdict

graph_ = defaultdict(list)

for line in inp_readlines():
    start, end = line.strip().split(")")
    graph_[start].append(end)

count = 0

graph = DGraph(graph_)

topsorted = graph.topsort("COM")

counts = {}
for v in topsorted[::-1]:
    counts[v] = sum([counts[w]+1 for w in graph[v]])


def path(start, end):
    (found, d) = graph.BFS(start, end)
    return d if found else 100000000000


print("Part 1:", sum(counts.values()))  # part 1

minorb = graph.sym().BFS("YOU").dist("SAN")

print("Part 2:", minorb-2)
