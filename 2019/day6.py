from utils2020 import DGraph
from collections import defaultdict

graph_ = defaultdict(list)

for line in open("input6").readlines():
    [start, end] = line.strip().split(")")
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

minorb = 10000000000000000
for i in topsorted:
    minorb = min(minorb, path(i, "YOU") + path(i, "SAN"))
    if i == "YOU" or i == "SAN":
        break

print(minorb-2)
