# pylint: disable=unused-wildcard-import
from utils import *

raw = [g.split("\n") for g in inp_groups()]


@dataclass(init=False, unsafe_hash=True)
class Rule:
    line: str

    def __init__(self, line):
        (l1, u1, l2, u2) = ints_in(line)
        self.name = line.split(":")[0]
        self.range1 = irange(l1, u1)
        self.range2 = irange(l2, u2)
        self.line = line
        self.pos = set()

    def __str__(self):
        return self.line

    def __contains__(self, num):
        return num in self.range1 or num in self.range2


def ticket(line):
    return tuple(ints(line.split(",")))


rules = [Rule(line) for line in raw[0]]

my_tick = ticket(raw[1][1])

ticks = [ticket(line) for line in raw[2][1:]]

valid = set()
invalid_nums = []

for tick in ticks:
    tv = True
    for num in tick:
        if not any(num in r for r in rules):
            invalid_nums.append(num)
            tv = False
    if tv:
        valid.add(tick)

print(invalid_nums)
print(sum(invalid_nums))

valid.add(my_tick)

for r in rules:
    r.pos = {p for p in range(len(my_tick)) if all(
        tick[p] in r for tick in valid)}
    print(r, r.pos)

fpos = pick_uniq({r: r.pos for r in rules})

print([fpos[r] for r in rules])

ans = [my_tick[fpos[r]]
       for r in rules if r.name.startswith("depart")]
print(ans, math.prod(ans))

# sanity check
for tick in valid:
    for r in rules:
        if tick[fpos[r]] not in r:
            print("Invalid!", r.name, tick)
