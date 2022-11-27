import intcode

prog = intcode.load_program()


def run(inp):
    return intcode.Machine(prog, inp).run()


print("Part 1:", run([1])[-1])
print("Part 2:", run([5])[-1])
