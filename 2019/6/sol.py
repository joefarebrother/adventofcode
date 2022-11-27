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


print(sum(counts.values()))  # part 1

_, minorb = graph.sym().BFS("YOU", "SAN")

print(minorb-2)
