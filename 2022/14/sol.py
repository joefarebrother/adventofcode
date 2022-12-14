from utils import *

gr = Grid()
lowest = defaultdict(lambda: -10000)

for line in inp_readlines():
    for p1, p2 in windows(chunks(ints_in(line), 2), 2):
        for p in Rectangle(p1, p2):
            gr[p] = "#"
            lowest[p.x] = max(lowest[p.x], p.y)

sand_spawner = IVec2(500, 0)

floor = max(lowest.values())+2

p1 = False

num_sand = 0
sand = sand_spawner
while True:
    if not p1 and sand.y > lowest[sand.x]:
        print("Part 1:", num_sand)
        p1 = True
    pts = [sand+(0, 1), sand+(-1, 1), sand+(1, 1)]
    for p in pts:
        if p.y != floor and gr[p] not in ["#", "o"]:
            sand = p
            break
    else:
        gr[sand] = "o"
        num_sand += 1
        if sand == sand_spawner:
            print("Part 2:", num_sand)
            exit()
        sand = sand_spawner
