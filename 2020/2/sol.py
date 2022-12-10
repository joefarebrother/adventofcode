# pylint: disable=unused-wildcard-import
from utils import *

data = inp_readlines()


def parse(line):
    (lo, hi, ch, pw) = re.fullmatch(r'(\d+)-(\d+) (.):(.*)', line).groups()
    return (int(lo), int(hi), ch, pw)


def valid(line):
    (lo, hi, ch, pw) = parse(line)
    cnt = list(pw).count(ch)
    return lo <= cnt <= hi


def valid2(line):
    (lo, hi, ch, pw) = parse(line)
    # since we don't strip the leading space in pw, we get 1-based indexing for free :)
    return (pw[lo] == ch) ^ (pw[hi] == ch)


print("Part 1:", sum(map(valid, data)))
print("Part 2:", sum(map(valid2, data)))
