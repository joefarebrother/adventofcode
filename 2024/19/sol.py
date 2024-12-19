from utils import *

opts, towels = inp_groups()
opts = opts[0].split(", ")

@cache 
def possible(towel):
    if not towel:
        return True 
    return any(possible(towel[len(opt):]) for opt in opts if towel.startswith(opt))

@cache 
def ways(towel):
    if not towel:
        return 1
    return sum(ways(towel[len(opt):]) for opt in opts if towel.startswith(opt))


print("Part 1:", sum(map(possible,towels)))
print("Part 2:", sum(map(ways,towels)))