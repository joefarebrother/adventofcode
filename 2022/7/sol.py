from utils import *

cmds = []

for line in inp_readlines():
    if line.startswith("$"):
        cmds.append((line[1:].strip(), []))
    else:
        cmds[-1][1].append(line)


@dataclass
class File:
    name: str
    size: int


@dataclass
class Dir:
    name: str
    parent: str
    files: dict = field(default_factory=dict)

    def everything_under(self):
        res = [self]
        for f in self.files.values():
            if isinstance(f, Dir):
                res += f.everything_under()
            else:
                res.append(f)
        return res

    def tot_size(self):
        return sum(f.size for f in self.everything_under() if isinstance(f, File))  # pylint:disable=no-member


root = Dir("/", None)

pwd = root

for (cmd, out) in cmds:
    if cmd.startswith("cd"):
        arg = cmd.split()[1]
        if arg == "/":
            pwd = root
        elif arg == "..":
            pwd = pwd.parent
        else:
            if arg in pwd.files:
                pwd = pwd.files[arg]
            else:
                # this doesn't happen on he real input or the test
                new = Dir(arg, pwd)
                pwd.files[arg] = new
                pwd = new
    elif cmd.startswith("ls"):
        for line in out:
            size, name = line.split()
            if name not in pwd.files:
                if size == "dir":
                    pwd.files[name] = Dir(name, pwd)
                else:
                    pwd.files[name] = File(name, int(size))
            else:
                # this doesn't happen on the real input or the test
                actual = pwd.files[name]
                assert actual.name == name
                if size == "dir":
                    assert isinstance(actual, Dir)
                else:
                    assert isinstance(actual, File)
                    assert actual.size == int(size)

tot = 0
for f in root.everything_under():
    if isinstance(f, Dir):
        sz = f.tot_size()
        if sz <= 100000:
            tot += sz
print("Part 1:", tot)

free = 70000000 - root.tot_size()
cand = [f for f in root.everything_under() if isinstance(f, Dir) and f.tot_size()+free >= 30000000]
print("Part 2:", min(f.tot_size() for f in cand))
