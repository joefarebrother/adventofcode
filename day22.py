from utils import *
inp = open("input22").readlines()

N = 119315717514047
#N=10007

# (i * a + b)%N = pos of card i
cards = (1, 0)

def rev(cards):
  # x -> N-1 - x = -1 - x = -(x+1)
  return ((-cards[0])%N, (-cards[1]-1)%N)

def cut(cards, n):
  return (cards[0], (cards[1]-n)%N)

def deal(cards, n):
  return ((cards[0]*n)%N, (cards[1]*n)%N)


for line in inp:
  if line.startswith("deal i"):
    cards = rev(cards)
  elif line.startswith("cut"):
    cards = cut(cards, int(line[3:].strip()))
  elif line.startswith("deal w"):
    cards = deal(cards, int(line[len("deal with increment"):].strip()))
  else:
    print ("Unknown: " + line)


#repeat a bunch

rep = 101741582076661

#i -> i*a + b
# rep n times
#i*a^2 + ab + b
#i*a^3 + a^2b + ab + b
#i*a^n + b*(sum j=0..n-1 a^j)
#i*a^n + b*(a^n-1)/(a-1)

a, b = cards
an = pow(a, rep, N)

A, B = an, b*(an-1) * mod_inv(a-1, N)
print((2019 * A + B) % N)

# want card in pos 2020
print((2020 - B)*mod_inv(A, N) % N)
