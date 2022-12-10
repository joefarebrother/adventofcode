# pylint: disable=unused-wildcard-import
from utils import *

data = inp_groups()

ans = 0
for grp in data:
    uniq = set(''.join(grp))
    print(uniq, len(uniq))
    ans += len(uniq)
print("Part 1:", ans)

ans = 0
for grp in data:
    all = set("qwertyuiopasdfghjklzxcvbnm")
    for per in grp:
        qs = set(per)
        all &= qs
    ans += len(all)
    print(ans, all)
print("Part 2:", ans)
