# pylint: disable=unused-wildcard-import
from utils import *
from itertools import *
import re

data = groups("input4", split=False)


def parse(gr):
    res = {}
    for field in gr.split():
        kv = field.split(":")
        if len(kv) == 2:
            k, v = kv
            res[k] = v

    res['cid'] = None
    return DotDict(res)


print(data)


def num(field, min, max):
    return min <= mint(field, 0) <= max


def valid(rec):
    if len(rec.keys()) != 8:
        return False

    return (num(rec.byr, 1920, 2002) and
            num(rec.iyr, 2010, 2020) and
            num(rec.eyr, 2020, 2030) and
            (150 <= match(r'(\d*)cm', rec.hgt, onfail=[0])[0] <= 193
             or 59 <= match(r'(\d*)in', rec.hgt, onfail=[0])[0] <= 76) and
            match(r'#[0-9a-f]{6}', rec.hcl) and
            rec.ecl in "amb blu brn gry grn hzl oth".split() and
            match(r'\d{9}', rec.pid))

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
for gr in data:
    p = parse(gr)
    if valid(p):
        print("valid: ", p)
        ans += 1
    else:
        print('invalid:', p)

print(ans)
