# pylint: disable=unused-wildcard-import
from utils import *

seats = readlines("input5")


def parse(seat: str):
    r = seat[:7]
    c = seat[-3:]

    rn = int(r.replace("F", "0").replace("B", "1"), base=2)
    cn = int(c.replace("L", "0").replace("R", "1"), base=2)

    return (rn, cn)


pseats = mapl(parse, seats)

ids = [rn*8+cn for (rn, cn) in pseats]

for i in range((min(ids)+1), max(ids)):
    if i-1 in ids and i+1 in ids and i not in ids:
        print(i)
