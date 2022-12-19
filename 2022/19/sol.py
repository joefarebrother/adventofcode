from utils import *


@dataclass(frozen=True)
class Resources:
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0

    def __add__(self, other):
        if isinstance(other, Resources):
            return Resources(self.ore+other.ore, self.clay+other.clay, self.obsidian+other.obsidian, self.geode+other.geode)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Resources):
            return Resources(self.ore-other.ore, self.clay-other.clay, self.obsidian-other.obsidian, self.geode-other.geode)
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Resources):
            return all([self.ore <= other.ore, self.clay <= other.clay, self.obsidian <= other.obsidian, self.geode <= other.geode])
        return NotImplemented

    def __getitem__(self, idx):
        return self.__getattribute__(idx)


class Blueprint:
    def __init__(self, gr):
        self.costs = {}

        if isinstance(gr, str):
            gr = gr.replace(":", ".").split(".")[:-1]

        self.id = only(ints_in(gr[0]))

        for line in gr[1:]:
            r, cs = match(r'.*Each (\w+) robot costs (.*)\.?', line)
            cs = cs.split(" and ")
            cs2 = Counter()
            for c in cs:
                amt, thing = c.split()
                amt = int(amt)
                thing = thing.strip(".")
                cs2[thing] = amt
            self.costs[r] = Resources(**cs2)

    def theoretical_maximum(self, time, stuff, robots):
        for _ in range(time):
            stuff += robots
            for r, cs in self.costs.items():
                if cs <= stuff:
                    robots += Resources(**{r: 1})
                    stuff -= cs
                    stuff += Resources(ore=cs.ore)
        return stuff.geode

    def redundant(self, res, time, amt, rob):
        if res == 'geode':
            return False
        maxc = max(cs[res] for cs in self.costs.values())
        return maxc * time <= amt + rob*time

    def geodes(self, time):
        best_poss = 0

        @cache
        def go(time, stuff, robots):
            nonlocal best_poss
            print(self.id, time, stuff, robots, best_poss)
            if time == 0:
                res = stuff.geode
                best_poss = max(best_poss, res)
                return res
            if self.theoretical_maximum(time, stuff, robots) <= best_poss:
                return 0
            nstuff = stuff + robots
            best = 0
            for r in ['geode', 'obsidian', 'clay', '', 'ore']:
                if r == '':
                    best = max(best, go(time-1, nstuff, robots))
                else:
                    cs = self.costs[r]
                    if cs <= stuff and not self.redundant(r, time, stuff[r], robots[r]):
                        nstuff2 = nstuff - cs
                        nrobots = robots + Resources(**{r: 1})
                        best = max(best, go(time-1, nstuff2, nrobots))
            res = best
            best_poss = max(best_poss, res)
            return res

        return go(time, Resources(), Resources(ore=1))

    def quality(self):
        return self.id * self.geodes(24)


inp = inp_groups() if is_ex else inp_readlines()
bs = [Blueprint(gr) for gr in inp]

if is_ex:
    print("Part 1: 33")
    # exit()
# print("Part 1:", sum(b.quality() for b in bs))

print("Part 2:", math.prod(b.geodes(32) for b in bs[:3]))
