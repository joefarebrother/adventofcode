from utils import *
data = readLines("input1")
print(data)
data = map(int, data)

def issum(num, xs):
  return sum(xs) == num

for i in data:
  for j in data:
    if issum(2020, [i, j]):
      print(i*j, i, j)
      # submit(i*j)
      
for i in data:
  for j in data:
    for k in data:
      if issum(2020, [i, j, k]):
        print(i*j*k, i, j, k)
        
      
