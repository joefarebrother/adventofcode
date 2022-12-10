from math import lcm
from utils import inp_readlines, ints_in


class Moon:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.xv, self.yv, self.zv = 0, 0, 0

    def vel_step(self):
        self.x += self.xv
        self.y += self.yv
        self.z += self.zv

    def grav_step(self, other):
        if self.x < other.x:
            self.xv += 1
        if self.x > other.x:
            self.xv -= 1

        if self.y < other.y:
            self.yv += 1
        if self.y > other.y:
            self.yv -= 1

        if self.z < other.z:
            self.zv += 1
        if self.z > other.z:
            self.zv -= 1

    def pot_energy(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def kin_energy(self):
        return abs(self.xv) + abs(self.yv) + abs(self.zv)

    def energy(self):
        return self.kin_energy()*self.pot_energy()

    def __str__(self):
        return "pos=<"+str(self.x)+", "+str(self.y)+", "+str(self.z)+">,vel=<"+str(self.xv)+", "+str(self.yv)+", "+str(self.zv)+">"


def inp():
    moons = []
    for line in inp_readlines():
        moons.append(Moon(*ints_in(line)))
    return moons


moons = inp()


def step_system(moons):
    for m in moons:
        for n in moons:
            m.grav_step(n)
    for m in moons:
        m.vel_step()

    # for m in moons:
        # print(m)
    return sum([m.energy() for m in moons])


for i in range(1, 1001):
    en = step_system(moons)
print("Part 1:", en)

moons = inp()

seen_states = []

axes = [[Moon(m.x, 0, 0) for m in moons], [Moon(m.y, 0, 0) for m in moons], [Moon(m.z, 0, 0) for m in moons]]


def axis_period(axis):
    seen_states = {}
    i = 0
    while True:
        state = str([(m.x, m.xv) for m in axis])
        if state in seen_states:
            return (seen_states[state], i-seen_states[state])
        else:
            seen_states[state] = i
            step_system(axis)
            i += 1


data = [axis_period(a) for a in axes]
starts = [s for (s, p) in data]
periods = [p for (s, p) in data]


print("Part 2:", max(starts) + lcm(periods[0], periods[1], periods[2]))
