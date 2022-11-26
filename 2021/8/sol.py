from utils import *

inp = readlines(8)

"""
  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg
"""

segs = ["abcefg", "cf", "acdeg", "acdfg", "bcdf",
        "abdfg", "abdefg", "acf", "abcdefg", "abcdfg"]

inp2 = []
for line in inp:
    (pat, out) = line.split("|")
    inp2.append((pat.split(), out.split()))

easy_lens = [len(segs[i]) for i in [1, 4, 7, 8]]

c = 0
for (pat, out) in inp2:
    c += sum(len(o) in easy_lens for o in out)

print("Part 1: ", c)


def process(pat, out):
    for perm in itertools.permutations("abcdefg"):
        mp = {a: b for a, b in zip(perm, "abcdefg")}

        def repl(s):
            return "".join(sorted(mp[c] for c in s))

        if all(repl(p) in segs for p in pat):
            out = [str(segs.index(repl(o))) for o in out]
            return int("".join(out))


print("Part 2: ", sum(process(pat, out) for pat, out in inp2))
