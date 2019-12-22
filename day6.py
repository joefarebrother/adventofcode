graph = {}
verts = []
for line in open("input6").readlines():
  [start, end] = line.strip().split(")")
  if start in graph:
    graph[start].append(end)
  else:
    graph[start] = [end]
  verts += [start, end]

verts = set(verts)
count = 0

topsorted = []
def topsort(v):
  global topsorted
  if v not in topsorted:
    topsorted.append(v)
    if v in graph:
      for w in graph[v]:
        topsort(w)

topsort("COM")

counts = {}
for v in topsorted[::-1]:
  if v in graph:
    counts[v] = sum([counts[w]+1 for w in graph[v]])
  else:
    counts[v] = 0

def path(start, end):
  if start == end:
    return 0
  elif start not in graph:
    return 100000000000000000
  else:
    return 1+min([path(next, end) for next in graph[start]])

print(sum(counts.values())) # part 1

minorb = 10000000000000000
for i in topsorted:
  minorb = min(minorb, path(i, "YOU") + path(i, "SAN"))
  if i == "YOU" or i == "SAN":
    break

print(minorb)
