import intcode

prog = intcode.load_program("input5")

def run(inp):
  return intcode.Machine(prog, inp).run()

print(run([1]))
print(run([5]))
