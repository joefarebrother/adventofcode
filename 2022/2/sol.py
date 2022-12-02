from utils import *

inp = [line.split() for line in inp_readlines()]


def result(fst, snd):
    """Returns 0 for a draw, 1 for a win, 2 for a loss"""
    assert (fst in [1, 2, 3] and snd in [1, 2, 3])
    return (snd-fst) % 3


tot = 0
for fst, snd in inp:
    fst = " ABC".find(fst)
    snd = " XYZ".find(snd)
    res = result(fst, snd)
    score = [3, 6, 0][res]+snd
    tot += score

print("Part 1:", tot)

tot = 0
for fst, res in inp:
    fst = " ABC".find(fst)
    res = "YZX".find(res)
    snd = mod_inc(fst+res, 3)
    assert res == result(fst, snd)
    score = [3, 6, 0][res]+snd

    tot += score

print("Part 2:", tot)
