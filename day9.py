import intcode 

#prog = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99] 
prog = intcode.load_program("input9")


def run(inp):
  return intcode.Machine(prog, inp).run()

print(run([1]))
print(run([2]))
