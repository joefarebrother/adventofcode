from utils import *

rocks = """
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##""".split("\n\n")
rocks = mapl(lambda gr: Grid(gr.strip().split(), y_is_down=False), rocks)

instrs = inp_readall().strip()

gr = Grid(y_is_down=False)
floor = 0
left = 0
right = 8
spawnx = 3
highest = floor
time = 0
rock_idx = 0

for x in irange(left, right):
    gr[x, floor] = "-"


def move_left(rp, rock):
    for p_in_r in rock:
        if rock[p_in_r] == "#":
            # print(p_in_r+rp)
            if (p_in_r+rp).x-1 == left or gr[p_in_r+rp-(1, 0)] == "#":
                return rp, False
    return rp-(1, 0), True


def move_right(rp, rock):
    for p_in_r in rock:
        if rock[p_in_r] == "#":
            if (p_in_r+rp).x+1 == right or gr[p_in_r+rp+(1, 0)] == "#":
                return rp, False
    return rp+(1, 0), True


def move_down(rp, rock):
    for p_in_r in rock:
        if rock[p_in_r] == "#":
            # print(p_in_r+rp)
            if (p_in_r+rp).y-1 == floor or gr[p_in_r+rp-(0, 1)] == "#":
                return rp, False
    return rp-(0, 1), True


def spawn_new_rock():
    global rock_idx
    rock = rocks[rock_idx % len(rocks)]
    rock_idx += 1
    return IVec2(spawnx, highest+3+rock.height()), rock


def draw():
    gr2 = Grid(gr)
    assert_good(rp, rock)
    for p_in_r in rock:
        if rock[p_in_r] == "#":
            np = rp + p_in_r
            gr2[np] = "@"
    for y in range(highest+5):
        gr2[left, y] = "|"
        gr2[right, y] = "|"

    gr2.draw(maxrows=40)


def assert_good(rp, rock):
    for p_in_r in rock:
        if rock[p_in_r] == "#":
            np = rp + p_in_r
            assert left < np.x < right, (left, np.x, right)
            assert gr[np] != "#"
            assert np.y > floor


def reachable():
    def adj(p):
        if gr[p] == "#" or p.y == floor:
            return
        for p0 in neighbours(p):
            if p.x not in [left, right] and p.y <= highest+1:
                yield p0
    res = set()
    miny = highest
    grph = FGraph(adj=adj)
    for p, _ in grph.BFS(IVec2(1, highest+1)):
        if gr[p] == "#" or p.y == floor:
            res.add((p.x, p.y))
            miny = min(miny, p.y)
    res2 = set()
    for x, y in res:
        res2.add((x, y-miny))
    return frozenset(res2)


rp, rock = spawn_new_rock()
heights = []

seen = {}


def do_step():
    global rp, rock, highest, time
    if instrs[time % len(instrs)] == "<":
        rp, _ = move_left(rp, rock)
    else:
        assert instrs[time % len(instrs)] == ">"
        rp, _ = move_right(rp, rock)
    assert_good(rp, rock)
    rp, succ = move_down(rp, rock)
    assert_good(rp, rock)
    time += 1
    if not succ:
        for p_in_r in rock:
            if rock[p_in_r] == "#":
                np = rp + p_in_r
                gr[np] = "#"
                highest = max(highest, np.y)

        rp, rock = spawn_new_rock()
        heights.append(highest)
        return True
    return False


while True:
    placed = do_step()
    if placed and rock_idx == 2023:
        print("Part 1:", highest)
        # break
    if placed:
        state = reachable(), time % len(instrs), rock_idx % len(rocks)
        if state in seen:
            print("!!!", time, rock_idx, highest)
            break
        seen[state] = highest, rock_idx, time

    if time < 10 or (rock_idx < 15 and placed):
        print(time, rock_idx, rp, highest, placed)
        draw()

last_h, last_r, last_t = seen[state]
reps = (1000000000000-rock_idx) // (rock_idx-last_r)
h_off = (highest-last_h)*reps
time += (time-last_t)*reps
rock_idx += (rock_idx-last_r)*reps

while True:
    placed = do_step()
    if placed and rock_idx == 1000000000001:
        break

print("Part 2:", highest + h_off)
