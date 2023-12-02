from utils import *

class Game:
    def __init__(self, line):
        g, line = line.split(":")
        self.id = ints_in(g)[0]

        shows = []
        for show in line.split(";"):
            r = defaultdict(int)
            for b in show.split(","):
                n,c = b.strip().split(" ")
                r[c] += ints_in(n)[0]
            shows.append(r)

        #print(self.id, shows)
        self.shows = shows

    def impossible(self):
        for g in self.shows:
            if g["red"] > 12 or g["blue"] > 14 or g["green"] > 13:
                return True
        return False
    
    def power(self):
        smol = defaultdict(int)

        for g in self.shows:
            for c in g:
                smol[c] = max(smol[c], g[c])

        return math.prod(smol.values())

games = mapl(Game, inp_readlines())

tot = 0
for g in games:
    if not g.impossible():
        print(g.id)
        tot += g.id

print("Part 1:", tot)
print("Part 2:", sum(g.power() for g in games))