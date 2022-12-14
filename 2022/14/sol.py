from utils import *

gr = Grid()
lowest = defaultdict(lambda: -10000)

for line in inp_readlines():
    for p1, p2 in windows(chunks(ints_in(line), 2), 2):
        for p in Rectangle(tuple(p1), tuple(p2)):
            gr[p] = "#"
            lowest[p.x] = max(lowest[p.x], p.y)

sand_spawner = IVec2(500, 0)

lowest = max(lowest.values())+2


def spawn_sand():
    sand = sand_spawner
    while True:
        # if sand.y > lowest[sand.x]:
        #     return False
        pts = [sand+(0, 1), sand+(-1, 1), sand+(1, 1)]
        for p in pts:
            if p.y != lowest and gr[p] not in ["#", "o"]:
                sand = p
                break
        else:
            gr[sand] = "o"
            if sand == sand_spawner:
                return False
            return True


s = 0
while spawn_sand():
    s += 1

print(s+1)
