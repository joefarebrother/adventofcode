from intcode import *
from utils import *

prog = load_program("input23")

idle_count = 0
nat_history = [-1]

def inpfun(m):
  global idle_count, nat_history
  name = int(m.name or 0)

  if all([len(q) == 0 for q in qs]):
    idle_count += 1
    if idle_count > 100000 and name == 0:
      print("idle")
      qs[0] += nat
      print(nat)
      if nat[1] == nat_history[-1]:
        print("part2", nat[1])
        exit()
      nat_history += [nat[1]]
  else:
    idle_count = 0  

  if len(qs[name]) == 0:
    return -1
  else:
    return qs[name].pop(0) 
  

nat = [0, 0]

def outfun(m, v):
  global nat
  if type(m.out) != list:
    m.out = []
  m.out += [v]
  if len(m.out) == 3:
    if m.out[0] == 255:
      print(m.out[2])
      nat = m.out[1:]
      m.out = []
      return
    qs[m.out[0]] += m.out[1:]
    m.out = []

machines = [Machine(prog, inpfun, outfun, name=i) for i in range(50)]

qs = [[i] for i in range(50)]

while True:
  for m in machines:
    m.step()
