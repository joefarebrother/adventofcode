from utils import *

inp = inp_groups()

scanners = []
for gr in inp:
    sc = []
    for line in gr[1:]:
        sc.append(ints_in(line))
    scanners.append(sc)


@dataclass
class Matrix:
    data: list[list]

    def __init__(self, data):
        assert len(set(len(r) for r in data)) == 1, "Uniform lengths expected"
        self.data = data

    def __getitem__(self, idx):
        row, col = idx
        return self.data[row][col]

    def width(self):
        return len(self.data[0])

    def height(self):
        return len(self.data)

    def __matmul__(self, other):
        if isinstance(other, Matrix):
            sw, sh = self.width(), self.height()
            ow, oh = other.width(), other.height()
            assert sw == oh, f"Cannot multiply {sh}x{sw} by {oh}x{ow}"
            res = [[0]*ow for _ in range(sh)]
            for row in range(sh):
                for col in range(ow):
                    s = 0
                    for k in range(sw):
                        s += self[row, k] * other[k, col]
                    res[row][col] = s
            return Matrix(res)
        if isinstance(other, list):
            res = self @ Matrix([[x] for x in other])
            return [res[i, 0] for i in range(len(other))]
        if isinstance(other, tuple):
            return tuple(self @ list(other))
        if isinstance(other, Vector):
            return Vector(self@other.data)
        return NotImplemented


@dataclass(unsafe_hash=True)
class Vector:
    data: tuple

    def __init__(self, data):
        self.data = tuple(data)

    def __getitem__(self, i):
        return self.data[i]

    def __add__(self, other):
        assert len(self.data) == len(other.data), (self, other)
        return Vector(self[i] + other[i] for i in range(len(self.data)))

    def __sub__(self, other):
        return Vector(self[i] - other[i] for i in range(len(self.data)))

    def man_dist(self, other):
        return sum(abs(self[i]-other[i]) for i in range(len(self.data)))


rotx = Matrix([[1, 0, 0],
               [0, 0, 1],
               [0, -1, 0]])

roty = Matrix([[0, 0, 1],
               [0, 1, 0],
               [-1, 0, 0]])

rotz = Matrix([[0, 1, 0],
               [-1, 0, 0],
               [0, 0, 1]])

id = Matrix([[1, 0, 0],
             [0, 1, 0],
             [0, 0, 1]])


all_rots = []
for i, j, k in it.product(range(4), repeat=3):
    A = id
    for _ in range(i):
        A @= rotx
    for _ in range(j):
        A @= roty
    for _ in range(k):
        A @= rotz
    if A not in all_rots:
        all_rots.append(A)

assert len(all_rots) == 24, len(all_rots)


@dataclass
class Scanner:
    id: int
    seen: list
    off: Vector = None
    rot: Matrix = None

    def known(self):
        return self.off is not None and self.rot is not None

    def adjusted_seen(self):
        if not self.known():
            return self.seen
        return [self.off + self.rot@s for s in self.seen]


scanners = [Scanner(i, [Vector(v) for v in seen])
            for i, seen in enumerate(scanners)]
scanners[0].off = Vector((0, 0, 0))
scanners[0].rot = id

# print(scanners)


def find_offset(pts1, pts2):
    c = Counter()
    for a, b in it.product(pts1, pts2):
        c[a-b] += 1
    off, freq = c.most_common(1)[0]
    if freq >= 12:
        return off


def match_scanners_from(i):
    new = set()
    sci = scanners[i]
    assert sci.known()
    seeni = sci.adjusted_seen()
    for j, scj in enumerate(scanners):
        if not scj.known():
            for r in all_rots:
                seenj = [r@s for s in scj.seen]
                off = find_offset(seeni, seenj)
                if off:
                    scj.rot = r
                    scj.off = off
                    assert len(set(seeni) & set(scj.adjusted_seen())) >= 12
                    new.add(j)
                    break
    return new


known = {0}
while known:
    nknown = set()
    for i in known:
        nknown |= match_scanners_from(i)
    known = nknown

assert all(sc.known() for sc in scanners)

beacons = set()
for sci in scanners:
    beacons |= set(sci.adjusted_seen())

print("Part 1", len(beacons))

maxd = 0
for sci, scj in it.combinations(scanners, 2):
    maxd = max(maxd, sci.off.man_dist(scj.off))

print("Part 2", maxd)
