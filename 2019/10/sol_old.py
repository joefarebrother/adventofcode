from utils import inp_readlines
from math import atan2
inp = list(inp_readlines())


def blocked_by(mypos, pos1, pos2):
    mx, my = mypos
    x1, y1 = pos1
    x2, y2 = pos2

    dx1, dy1 = (mx-x1, my-y1)
    dx2, dy2 = (mx-x2, my-y2)

    return angle(mypos, pos1) == angle(mypos, pos2) and dx1**2 + dy1**2 > dx2**2 + dy2**2


def can_see(mypos, pos1):
    for pos2 in asteroids:
        if not (pos2 == mypos) and blocked_by(mypos, pos1, pos2):
            return False
    return True


def vis(mypos):
    count = 0
    for pos in asteroids:
        if not pos == mypos:
            if can_see(mypos, pos):
                count += 1
    return count


def angle(mypos, pos):
    x, y = pos
    mx, my = mypos
    return atan2(y-my, x-mx)


asteroids = []
for my in range(0, len(inp)):
    for mx in range(0, len(inp[0])):
        if inp[my][mx] == "#":
            asteroids.append((mx, my))

asteroids = set(asteroids)

maxcount = 0
maxpos = (0, 0)
for mypos in asteroids:
    count = vis(mypos)
    maxcount = max(count, maxcount)
    if maxcount == count:
        maxpos = mypos

print(maxpos)
print("Part 1:", maxcount)


cur_angle = atan2(-1, 0)
mypos = maxpos

count = 0
# special case: straight  up
for y in range(mypos[1], -1, -1):
    if (mypos[0], y) in asteroids:
        asteroids.remove((mypos[0], y))
        count += 1
        break

print(cur_angle)

while count < 201:
    min_next_angle = 1000
    min_next_pos = (0, 0)
    min_angle = 1000
    min_pos = (0, 0)

    for pos in asteroids:
        if can_see(mypos, pos):
            this_angle = angle(mypos, pos)
            if this_angle < min_angle:
                min_angle = this_angle
                min_pos = pos
            if this_angle < min_next_angle and this_angle > cur_angle:
                min_next_angle = this_angle
                min_next_pos = pos

    if min_next_angle == 1000:
        to_remove = min_pos
        cur_angle = min_angle
    else:
        to_remove = min_next_pos
        cur_angle = min_next_angle
    asteroids.remove(to_remove)
    x, y = to_remove
    count += 1
    print(str(count) + ": (" + str(x) + ", " +
          str(y) + ") at " + str(cur_angle), flush=True)
    if count == 200:
        print("Part 2:", 100*x+y)
