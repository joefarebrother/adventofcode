import intcode

#prog = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
prog = intcode.load_program()


def run(inp):
    return intcode.Machine(prog, inp).run()


print("Part 1:", run([1])[0])
print("Part 2:", run([2])[0])
