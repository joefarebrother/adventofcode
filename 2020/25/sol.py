# pylint: disable=unused-wildcard-import
from utils import *

keys = ints(inp_readlines())
#keys = [5764801, 17807724]

# transform(sub): subject ^ loop_size % 20201227
# keys = transform(7, loop_1), transform(7, loop_2)
# answer = transform(key_1, loop_2) = transform(key+2, loop_1) = 7 ^ (loop_1*loop_2)

MOD = 20201227


def find_loop(key):
    i = 0
    tr = 1
    while True:
        i += 1
        tr *= 7
        tr %= MOD
        if tr == key:
            return i


loops = mapl(find_loop, keys)
print(loops)
print(pow(7, math.prod(loops), MOD))
