# pylint: disable=unused-wildcard-import
from utils import *

data = groups("input6")

# ans = 0
# for i in data:
#     uniq = set(filter(lambda c: c.islower(), list(i)))
#     print(uniq, len(uniq))
#     ans += len(uniq)
#     print(ans)

print(data)

ans = 0
for grp in data:
    all = set(list("qwertyuiopasdfghjklzxcvbnm"))
    for per in grp.split("\n"):
        qs = set(filter(lambda c: c.islower(), list(per)))
        all &= qs
    ans += len(all)
    print(ans, all)
