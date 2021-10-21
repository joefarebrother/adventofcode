# pylint: disable=unused-wildcard-import
from utils import *

rules, ms = groups("19.in")

prules = {}
for r in rules.split("\n"):
    idx, rule = r.split(":")
    prules[int(idx)] = rule.strip()


@cache
def to_re(r, depth=0):
    try:
        i = int(r)
        if i == 8:
            return f'(?:{to_re(42)})+'
        if i == 11:
            if depth < 10:
                return f'(?:{to_re(42)}{to_re(11, depth+1)}?{to_re(31)})'
            else:
                return f'(?:{to_re(42)}{to_re(31)})'

        ex = prules[i]
        return "(?:" + "|".join("".join(to_re(i.strip()) for i in part.split(" ")) for part in ex.split("|")) + ")"
    except ValueError:
        if len(r) > 0 and r[0] == '"':
            return r[1]
        return ""


print(to_re(42), to_re(31))

print(to_re(0))
p = re.compile(to_re(0))


t = 0
for m in ms.split("\n"):
    if p.fullmatch(m):
        print(True, m)
        t += 1
    else:
        print(False, m)

print(t)
