# pylint: disable=unused-wildcard-import
from utils import *

raw = [g.split("\n") for g in groups("16.in")]


class Rule:
    def __init__(self, line):
        (n, l1, u1, l2, u2) = match(
            r'([\w ]+): (\d+)-(\d+) or (\d+)-(\d+)', line)
        self.name = n
        self.range1 = irange(l1, u1)
        self.range2 = irange(l2, u2)
        self.line = line
        self.fpos = None
        self.pos = set()

    def __str__(self):
        return self.line

    def __contains__(self, num):
        return num in self.range1 or num in self.range2

    def positions(self):
        """Unnecassary once input is handled correctly"""
        if self.fpos != None:
            yield self.fpos
        else:
            yield from self.pos


class Ticket:
    def __init__(self, line):
        self.fields = tuple(ints(line.split(",")))

    def __str__(self):
        return str(self.fields)


rules = [Rule(line) for line in raw[0]]

my_tick = Ticket(raw[1][1])

ticks = [Ticket(line) for line in raw[2][1:]]

valid = set()
invalid = set()
invalid_nums = []

for tick in ticks:
    tv = True
    for num in tick.fields:
        for rule in rules:
            if num in rule:
                break
        else:
            invalid.add(tick)
            invalid_nums.append(num)
            tv = False
            continue
    if tv:
        valid.add(tick)

print(invalid_nums)
print(sum(invalid_nums))

valid.add(my_tick)

for r in rules:
    positions = set()
    for p in range(len(my_tick.fields)):
        for tick in valid:
            if tick.fields[p] not in r:
                break
        else:
            positions.add(p)
    r.pos = positions
    print(r, r.pos)

fixed = set()
while True:
    for r in rules:
        if len(r.pos) == 1:
            p = list(r.pos)[0]
            fixed.add(p)
            r.fpos = p
            break
    else:
        break
    for r in rules:
        if p in r.pos:
            r.pos.remove(p)

print(fixed, [(r.pos) for r in rules])

# # this turned out to be unnecassary once I handled my input correctly
# taken = set()
# def solve(ridx):
#     if ridx == len(rules):
#         return True
#     print([r.fpos for r in rules], ridx)
#     r = rules[ridx]
#     for p in r.positions():
#         if p not in taken:
#             taken.add(p)
#             old_fpos = r.fpos
#             r.fpos = p
#             if solve(ridx+1):
#                 return True
#             else:
#                 taken.remove(p)
#                 r.fpos = old_fpos
#     return False
# print(solve(0))

print([r.fpos for r in rules])

ans = [my_tick.fields[r.fpos]
       for r in rules if r.name.startswith("depart")]
print(ans, math.prod(ans))

for tick in valid:
    for r in rules:
        if tick.fields[r.fpos] not in r:
            print("Invalid!", r.name, tick)
