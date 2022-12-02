from utils import *

tot = 0
for line in inp_readlines():
    if line:
        fst, snd = line.split(" ")
        fst = " ABC".find(fst)
        snd = " XYZ".find(snd)
        assert (fst in [1, 2, 3] and snd in [1, 2, 3])
        score = [3, 6, 0][(snd-fst) % 3]+snd
        print(fst, snd, score)
        tot += score

tot = 0
for line in inp_readlines():
    if line:
        fst, res = line.split(" ")
        fst = " ABC".find(fst)
        res = {"X": -1, "Y": 0, "Z": 1}[res]
        snd = mod_inc(fst+res, 3)
        assert (fst in [1, 2, 3] and snd in [1, 2, 3])
        score = [3, 6, 0][res]+snd
        print(fst, snd, score)
        tot += score

print(tot)
