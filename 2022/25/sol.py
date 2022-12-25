from utils import *

inp = inp_readlines()


def from_snafu(x):
    s = 0
    for p, d in enumerate(x[::-1]):
        s += 5**p * {'0': 0, '1': 1, '2': 2, '-': -1, '=': -2}[d]
    return s


def to_snafu(x):
    s = ''
    while x:
        d = (x+2) % 5-2
        s += inv_mapping({'0': 0, '1': 1, '2': 2, '-': -1, '=': -2})[d]
        x -= d
        x //= 5
    return s[::-1]


s = 0
for line in inp:
    x = from_snafu(line)
    y = to_snafu(x)
    assert line == y, (line, x, y)
    s += x

print(to_snafu(s))
