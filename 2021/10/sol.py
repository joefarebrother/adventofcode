from utils import *

inp = readlines(10)

"""

    ): 3 points.
    ]: 57 points.
    }: 1197 points.
    >: 25137 points.

"""

close = {"{": "}", "(": ")", "[": "]", "<": ">"}
score = {")": 3, "]": 57, "}": 1197, ">": 25137}
score2 = {")": 1, "]": 2, "}": 3, ">": 4}

"""

    ): 1 point.
    ]: 2 points.
    }: 3 points.
    >: 4 points.

"""


def process(line):
    stk = []
    for c in line:
        if c in close:
            stk.append(close[c])
        else:
            if stk[-1] == c:
                stk.pop()
            else:
                return (True, score[c])
    sc = 0
    for i, c in enumerate(reversed(stk)):
        sc *= 5
        sc += score2[c]
    return (False, sc)


incorrect = []
incomplete = []
for err, sc in map(process, inp):
    if err:
        incorrect.append(sc)
    else:
        incomplete.append(sc)

print("Part 1: ", sum(incorrect))
incomplete = sorted(incomplete)
print("Part 2: ", incomplete[len(incomplete)//2])
