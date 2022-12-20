from utils import *
import dataclasses


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

    def __mul__(self, other):
        if isinstance(other, int):
            return Resources(self.ore*other, self.clay*other, self.obsidian*other, self.geode*other)
        return NotImplemented

    __rmul__ = __mul__

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
        def go(time, stuff, robots, skipped=Resources()):
            nonlocal best_poss
            # print(self.id, time, stuff, robots, best_poss)
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
                    # if we skip building a robot, don't consider building it next turn
                    skipped2 = skipped
                    for r2, cs in self.costs.items():
                        if cs <= stuff:
                            skipped2 += Resources(**{r2: 1})
                    best = max(best, go(time-1, nstuff, robots, skipped2))
                else:
                    cs = self.costs[r]
                    if cs <= stuff and not skipped[r] and not self.redundant(r, time, stuff[r], robots[r]):
                        nstuff2 = nstuff - cs
                        nrobots = robots + Resources(**{r: 1})
                        best = max(best, go(time-1, nstuff2, nrobots))
            res = best
            best_poss = max(best_poss, res)
            return res

        return go(time, Resources(), Resources(ore=1))

    def geodes_using_astar(self, time):
        big_number = 0

        # proof of correctness:
        # goal state: timestep 0.
        # distance to any given step from the start state = big_number*time - geodes
        # if big_number were, say, 10000, then all edge weights are nonnegative.
        # the heuristic is admissible; as theoretical_maximum is an upper bound on the number of geodes producible, so it never overestimates distance.
        # thus, astar correctly finds the shortest path. (i.e. that with the maximum produced geodes)
        # now, at each step, astar picks the node with minimum
        # d+h = (big_number*time) - geodes_so_far + (big_number*time_remaining) - upper_bound_on_remaining_geodes
        # = (big_number*total_time) - geodes_so_far -  upper_bound_on_remaining_geodes
        # = (big_number*total_time) + d' + h', where d' and h' are the distance/heuristic functions i the case big_number = 0.
        # thus, in the case big_number = 0, the same result is produced.
        # this allows the edges from essential leaves to a goal node to be removed, as their weight would just be 0. This makes it faster.

        # the reason this doesn't work with djikstra (i.e. h=0) is that h=0 is not admissible when there are negative weights.

        # alternative proof that works on any graph with negative weights and a consistent heuristic,
        # not just a graph in which we can add costs to each time step like this:
        # h is consistent, i.e. h(x) <= d(x,y) + h(y)
        # this makes A* equiv to djikstra with d'(x,y) = h(y) - h(x) + d(x,y)
        # this is a graph with nonnegative weights, so djikstra minimises d'(start, end); which minimizes d(start,end) as h(start) and h(end) are constant.

        # in fact, the first proof can be adapted to any DAG where we don't have explicit timesteps. Order the nodes topologically,
        # and put all goal nodes at the end. Then assign each node a timestamp based on the order it appears, with all goal nodes receiving the same timestamp.
        # then the above proof works. We also need h(goal) to be constant (ideally 0).

        def h(node):
            time, stuff, robots = node
            if time == 0:
                return 0
            best = self.theoretical_maximum(time, stuff, robots)
            return big_number*time - best

        def adj(node):
            time, stuff, robots = node
            res = {}
            # res[0, stuff, robots] = big_number*time
            if time <= 1:
                return res
            for rob in ['ore', 'clay', 'obsidian', 'geode']:
                # try to build a robot
                costs_dict = dataclasses.asdict(self.costs[rob])
                if any(robots[r] == 0 for r, c in costs_dict.items() if c > 0):
                    # if we have no robots to produce anything in the cost of rob, skip
                    continue

                if self.redundant(rob, time, stuff[rob], robots[rob]):
                    continue

                max_steps = 0
                for r, c in costs_dict.items():
                    if c > 0:
                        max_steps = max(max_steps, (c-stuff[r]-1)//robots[r]+1)
                tt = max_steps+1

                geodes = (time-tt)*(rob == 'geode')
                if time-tt > 0:
                    nstuff = stuff+robots*tt-self.costs[rob]
                    nrobots = robots + Resources(**{rob: int(rob != "geode")})
                    res[time-tt, nstuff, nrobots] = big_number*tt-geodes

            return res

        gr = FGraph(adj=adj)
        node, dist = gr.astar(start=(time, Resources(), Resources(ore=1)), h=h).find(lambda n: n[0] == 0 or len(adj(n)) == 0)

        print(time, node, big_number*time-dist)
        return big_number*time - dist

    def quality(self):
        return self.id * self.geodes_using_astar(24)


inp = inp_groups() if is_ex else inp_readlines()
bs = [Blueprint(gr) for gr in inp]

print("Part 1:", sum(b.quality() for b in bs))

print("Part 2:", math.prod(b.geodes_using_astar(32) for b in bs[:3]))
