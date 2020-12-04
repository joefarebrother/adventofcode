# pylint: disable=unused-wildcard-import
from utils import *

data = list(open("input2"))

data = mapl(lambda l: l.split(":"), data)


def parse_pol(pol):
    (lo, hi) = ints_in(pol)
    char = pol[-1]
    return (lo, hi, char)


def valid(pol, pw):
    (lo, hi, ch) = parse_pol(pol)
    cnt = list(pw).count(ch)
    return lo <= cnt <= hi


def valid2(pol, pw):
    (lo, hi, ch) = parse_pol(pol)
    # since we don't strip the leading space in pw, we get 1-based indexing for free :)
    return (pw[lo] == ch) ^ (pw[hi] == ch)


validcount = 0
for (pol, pw) in data:
    if valid2(pol, pw):
        validcount += 1

print(validcount)
