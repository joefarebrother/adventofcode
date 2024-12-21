from utils import *

inp = inp_readlines()

keypad0 = """789
456
123
 0A"""

keypad1 = """ ^A
<v>"""

keypad2 = keypad1 

def ways(seq, keypad):
    subseq = []
    for a,b in windows("A" + seq, 2):
        subseq.append(ways_pair(a,b,keypad))
    for ss in itertools.product(*subseq):
        yield "A".join(ss)+"A"

def ways_pair(a,b, keypad):
    g = Grid(keypad.split("\n"))
    #print(sorted())
    pa = g.index(a)
    pb = g.index(b)

    # need the arrangements of num x changes and num y changes
    def go(pa,pb):
        dx = sign(pa.x - pb.x)
        dy = sign(pa.y - pb.y)

        if pa == pb:
            yield ""
            return 
        
        if dx != 0:
            npb = pb + P(dx,0)
            if g[npb] != " ":
                for r in go(pa,npb):
                    yield r + " <>"[dx]
        if dy != 0:
            npb = pb + P(0,dy)
            if g[npb] != " ":
                for r in go(pa,npb):
                    yield r + " ^v"[dy]

    
    yield from go(pa,pb)



def overall_ways_p1(seq):
    ways0 = ways(seq, keypad0)

    best = []
    bestl = 100000
    for way in ways0:
        # print("way0", way)
        ways1 = ways(way, keypad1)

        l = len(next(ways1))
        if l < bestl:
            best = []
            bestl = l

        best.append(way)

    ways1 = [way for way0 in best for way in ways(way0, keypad1) ]

    # print("ways1", ways1)

    best = []
    bestl = 100000
    for way in ways1:
        ways2 = ways(way, keypad2)

        l = len(next(ways2))
        if l < bestl:
            best = []
            bestl = l

        best.append(way)
    
    # print("p1:", seq, next(ways(best[0], keypad2)))
    return bestl

def prune_ways(ways0):
    ways0 = list(ways0)
    if len(ways0) <= 1:
        return ways0
    #print("prune", ways0)
    best = []
    bestl = 100000
    for way in ways0:
        #print("way0", way)
        ways1 = ways(way, keypad1)

        l = len(next(ways1))
        if l < bestl:
            best = []
            bestl = l

        best.append(way)
    #print("pruneres", ways0, best)
    return best

def waysp(seq, keypad):
    subseq = []
    for a,b in windows("A" + seq, 2):
        # wp = list(ways_pair(a,b,keypad))
        #print("waysp", a, b, wp)
        subseq.append(prune_ways(ways_pair(a,b,keypad)))
    for ss in itertools.product(*subseq):
        yield "A".join(ss)+"A"



@cache
def best_way(seq, pads):
    if pads == 0:
        w = list(ways(seq, keypad1))
        assert len(set(len(l) for l in w)) == 1
        return len(w[0])
    
    ways0 = list(ways(seq, keypad1))
    # print("best_way", seq, pads, ways0)
    ways_by_len = {}
    for way in ways0:
        way_split = [x+"A" for x in way.split("A")]
        best = [best_way(w, pads-1) for w in way_split]
        # print(way_split, best)
        ways_by_len[way] = sum(b for b in best)


    return min(ways_by_len.values())-1

def overall_ways2(seq, pads=24):
    ways0 = list(ways(seq, keypad0))
    #pads = 24
    res = min([best_way(w, pads) for w in ways0])


    # print("p2:", seq, res)
    return res

# debugging rewrite compared to orig
# @cache
# def len_best_way(seq, pads):
#     """Returns the length of the best way to input the given sequence on `pads` layers of pads"""

#     return sum(len_best_way_pair(a,b,pads) for a,b in windows("A"+seq, 2))
    
# @cache
# def len_best_way_pair(a,b, pads):
#     """Returns the length of the best way to get from a to b and press A on `pad` layers of pads"""

#     if pads == 0:
#         return 1 
    
#     if type(pads) == tuple:
#         pad, npads = pads 
#     else:
#         pad, npads = keypad1, pads-1 

#     return min(lbw2(seq, npads) for seq in ways_pair_2(a,b,pad))

# def lbw2(seq, pads):
#     if pads >= 2:
#         r1 = best_way_1(seq, pads-1)
#         r2 = len_best_way(seq, pads)
#         assert r1 == r2, (seq, pads, r1, r2)
#         return r1 
#     return len_best_way(seq, pads)

# def ways_pair_2(a,b, keypad):
#     """Return the (up to) 2 sensible ways to get from a to b, then press A"""
#     g = Grid(keypad.split("\n"))
#     pa = g.index(a)
#     pb = g.index(b)

    
#     diff = pa - pb 

#     dx = diff.x
#     wx = " <>"[sign(dx)]*abs(dx) 
#     dy = diff.y
#     wy = " ^v"[sign(dy)]*abs(dy)

#     res = []
#     if g[pa-(dx,0)] != " ":
#         res.append(wx+wy+"A")
#     res.append(wy+wx+"A")

#     return list(set(res))

# @cache
# def best_way(seq, pads):
#     r1 = best_way_1(seq, pads)
#     r2 = len_best_way(seq, pads+1)
#     # assert r1 == r2, (seq, pads, r1, r2)
#     return r1

#for i in range(1,25):
ans = 0
for seq in inp:
    #print(seq, overall_ways_p1(seq), overall_ways2(seq))
    ans += int(seq[:-1]) * overall_ways2(seq)
    #print(i+1, ans)

def play(way, keypad=keypad1):
    g = Grid(keypad.split("\n"))
    res = ""
    p = g.index("A")
    for x in way:
        if x == "A":
            res += g[p]
        else:
            p += Dirs[x]
    return res 

way1a =     "v<A<AA>^>AvA^<A>AAAvA^Av<A<A>^>"
way1b = "v<<A>>^AAAv<A<A>>^AvAA^<A>Av<A<A>>^"
print((play(way1a)))
print((play(way1b)))
print(play(play(way1a)))
print(play(play(way1b)))

print(ans)
# print(0)