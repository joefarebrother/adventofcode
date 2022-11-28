from utils import *

inp = Grid(0)
asteroids = set(p for p, v in inp.items() if v == "#")

by_angle = defaultdict(lambda: defaultdict(list))
for p in asteroids:
    for q in asteroids:
        by_angle[p][angle(p, q)].append(q)

best_pos, best_view = max(by_angle.items(), key=lambda pv: len(pv[1]))
print("Part 1:", best_pos, len(best_view))

# y is down; so -1j points up and angles increase clockwise
cur_angle = angle(-1j)

angles = sorted(list(best_view))
next_angle = {a: b for (a, b) in windows(angles, 2)}
next_angle[angles[-1]] = angles[0]

view = {ang: sorted(asts, key=lambda ast: dist(best_pos, ast))
        for ang, asts in best_view.items()}

for count in irange(max(len(asteroids)-1, 201)):
    destroyed = view[cur_angle].pop(0)
    x, y = destroyed
    print(f"{count}: {(x,y)} at {cur_angle}")
    if count == 200:
        print("Part 2:", 100*x+y)

    cur_angle = next_angle[cur_angle]
    while not view[cur_angle]:
        cur_angle = next_angle[cur_angle]
