inp = open("input14").readlines()

react = {}

for line in inp:
  spl = line.split('=>')
  rhs = spl[1].strip().split()
  lhs_ = spl[0].strip().split(",")
  lhs = []
  for w_ in lhs_:
    w = w_.strip().split()
    lhs.append((int(w[0]), w[1]))
 
  react[rhs[1]] = (int(rhs[0]), lhs)

#for rhs in react:
#  print(rhs, react[rhs])


def balanced(amts):
  return all([chem == "ORE" or amts[chem] >= 0 for chem in amts.keys()])

def balance(amts):
  while not balanced(amts):
    for chem in amts:
      if chem != "ORE" and amts[chem] < 0:
        debt = -amts[chem]
        myamt, lhs = react[chem]
        rep = (debt+myamt-1)//myamt
        amts[chem] += rep*myamt
        for (n, c) in lhs:
          if c not in amts:
            amts[c] = 0
          amts[c] -= rep*n
        break

def ore_for_fuel(fuel):
  amts = {"FUEL":-fuel}
  balance(amts)
  return -amts["ORE"]

budget = 1000000000000

low = 1
high = 10
amt = 0

while amt <= budget:
  low, high = high, high*10
  amt = ore_for_fuel(high)
  print(amt)

# invariant: f(low) <= b < f(high)
while high-low > 1:
  mid = (high+low)//2
  amt = ore_for_fuel(mid)
  print(mid, amt)
  if amt > budget:
    high = mid
  else:
    low = mid

print(mid)
