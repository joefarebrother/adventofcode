from utils import *
data = ints(list(open("input1")))

for i in data:
  for j in data:
    if i+j == 2020:
      print(i*j, i, j)
      # submit(i*j)
      
for i in data:
  for j in data:
    for k in data:
      if i+j+k == 2020:
        print(i*j*k, i, j, k)
        
      
