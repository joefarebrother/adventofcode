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


validcount = 0
for line in data:
    if valid2(line):
        validcount += 1

print(validcount)
