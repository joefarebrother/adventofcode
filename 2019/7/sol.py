import itertools
from intcode import Machine, load_program

prog = load_program()


def run(part2):
    max_out = 0
    rng = range(5, 10) if part2 else range(5)
    for perm in itertools.permutations(list(rng)):
        inp_bufs = [[p] for p in perm]
        inp_bufs[0].append(0)

        machines = [Machine(prog, inp_bufs[i], inp_bufs[i-1]) for i in range(0, 5)]

        # print(perm)

        while not all([m.halted for m in machines]):
            for m in machines:
                m.step()

        out = inp_bufs[0][-1]
        max_out = max(out, max_out)
    return max_out


print("Part 1", run(False))
print("Part 2", run(True))
