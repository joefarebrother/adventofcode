from utils import *

rucks = []
for line in inp_readlines():
    half = len(line)//2
    c1, c2 = line[:half], line[half:]
    rucks.append((set(c1), set(c2)))


def pri(s: str):
    if s.isupper():
        return ord(s)-ord("A")+27
    else:
        return ord(s)-ord("a")+1


print("Part 1:", sum(pri(only(c1 & c2)) for (c1, c2) in rucks))

rucks = [c1 | c2 for (c1, c2) in rucks]

print("Part 2:", sum(pri(only(c1 & c2 & c3))
      for (c1, c2, c3) in chunks(rucks, 3)))
