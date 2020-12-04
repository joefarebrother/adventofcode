# pylint: disable=unused-wildcard-import
from utils import *
from itertools import *
import re

data = open("input4").read().split("\n\n")


def parse(line):
    res = {}
    for field in line.split():
        kv = field.split(":")
        if len(kv) == 2:
            k, v = kv
            res[k] = v

    res['cid'] = None
    return AttrDict(res)


print(data)


def num(field, min, max):
    return mint(field, -math.inf) in irange(min, max)


def valid(rec):
    if len(rec.keys()) != 8:
        return False

    return (num(rec.byr, 1920, 2002) and
            num(rec.iyr, 2010, 2020) and
            num(rec.eyr, 2020, 2030) and
            (re.fullmatch(r'\d*cm', rec.hgt) and int(rec.hgt[:-2]) in irange(150, 193)
             or re.fullmatch(r'\d*in', rec.hgt) and int(rec.hgt[:-2]) in irange(59, 76)) and
            re.fullmatch('^#[0-9a-f]{6}$', rec.hcl) and
            rec.ecl in "amb blu brn gry grn hzl oth".split() and
            re.fullmatch(r'\d{9}', rec.pid))

    # byr (Birth Year) - four digits; at least 1920 and at most 2002.
    # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    # hgt (Height) - a number followed by either cm or in:
    #     If cm, the number must be at least 150 and at most 193.
    #     If in, the number must be at least 59 and at most 76.
    # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    # pid (Passport ID) - a nine-digit number, including leading zeroes.
    # cid (Country ID) - ignored, missing or not.


ans = 0
for line in data:
    p = parse(line)
    if valid(p):
        print("valid: ", p)
        ans += 1
    else:
        print('invalid:', p)

print(ans)
