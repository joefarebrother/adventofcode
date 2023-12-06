from utils import *

times, dists = inp_readlines()
races = zip(*mapl(ints_in, [times,dists]))

def time(held, tot):
    return (tot-held)*held

def ways(td):
    t, d = td
    r = 0
    for h in range(t):
        if time(h, t) > d:
            r += 1
    return r 

print("Part 1:", math.prod(map(ways, races)))

race = ints_in(times.replace(" ", ""))[0], ints_in(dists.replace(" ", ""))[0]

def ways_smart(td):
    t, d = td

    h1 = bin_search(0, t//2, lambda h: time(h,t) <= d)
    h2 = bin_search(t//2, t, lambda h: time(h,t) > d)

    return h2 - h1

print("Part 2:", ways_smart(race))