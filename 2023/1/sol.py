from utils import *

tot = 0

# for line in inp_readlines():
#     ints = [c for c in line if c in "1234567890"]
#     tot += int(ints[0]+ints[-1])
#
# print("Part 1:", tot)

digs = ["zero","one","two","three","four","five","six","seven","eight","nine"]

def first_dig(f):
    for pre in prefixes(f):
        for dig in range(10):
            if str(dig) in pre or digs[dig] in pre:
                return dig
    print(f)
            
def last_dig(f):
    for post in suffixes(f):
        for dig in range(10):
            if str(dig) in post or digs[dig] in post:
                return dig
    print(f)


tot = 0
for line in inp_readlines():
    v = 10*first_dig(line) + last_dig(line)
    tot += v

print("Part 2:", tot)
    