from utils import *

tot = 0

# for line in inp_readlines():
#     ints = [c for c in line if c in "1234567890"]
#     tot += int(ints[0]+ints[-1])

digs = ["zero","one","two","three","four","five","six","seven","eight","nine"]


def first_dig(f):
    for pre in [f[:x] for x in range(len(f)+1)]:
        for dig in range(10):
            if str(dig) in pre or digs[dig] in pre:
                return dig
    print(f)
            
def last_dig(f):
    for post in [f[x:] for x in reversed(range(len(f)+1))]:
        for dig in range(10):
            if str(dig) in post or digs[dig] in post:
                return dig
    print(f)


tot = 0
for line in inp_readlines():
    v = 10*first_dig(line) + last_dig(line)
    tot += v

print(tot)
    