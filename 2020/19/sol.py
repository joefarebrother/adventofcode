# pylint: disable=unused-wildcard-import
from utils import *

rules, ms = inp_groups()

prules = {}
for r in rules:
    idx, rule = r.split(":")
    prules[int(idx)] = rule.strip()


@cache
def to_re(r, depth=0):
    try:
        i = int(r)
        if depth >= 0:
            if i == 8:
                return f'(?:{to_re(42)})+'
            if i == 11:
                if depth < 10:
                    return f'(?:{to_re(42)}{to_re(11, depth+1)}?{to_re(31)})'
                else:
                    return f'(?:{to_re(42)}{to_re(31)})'

        ex = prules[i]
        return "(?:" + "|".join("".join(to_re(i.strip(), depth) for i in part.split(" ")) for part in ex.split("|")) + ")"
    except ValueError:
        if len(r) > 0 and r[0] == '"':
            return r[1]
        return ""


p1re = re.compile(to_re(0, -1))
p2re = re.compile(to_re(0))

print("Part 1:", sum(bool(re.fullmatch(p1re, m)) for m in ms))
print("Part 2:", sum(bool(re.fullmatch(p2re, m)) for m in ms))
