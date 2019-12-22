from collections import defaultdict

def load_program(file): 
  return list(map(int, open(file).read().split(",")))

op_lens = {1:4, 2:4, 3:2, 4:2, 5:3, 6:3, 7:4, 8:4, 9:2}

def default_inpfun(self):
  if self.inp_ptr >= len(self.inp):
    return "wait"
  else:
    val = self.inp[self.inp_ptr]
    self.inp_ptr += 1
    return val

def default_outfun(self, val):
  self.out.append(val)

def ascii_input(self):
  if type(self.inp) != str:
    self.inp = ""
  if len(self.inp) <= self.inp_ptr:
    self.inp = input()+'\n'
    self.inp_ptr = 0
  val = self.inp[self.inp_ptr]
  self.inp_ptr += 1
  return ord(val)

def ascii_output(self, val):
  if type(self.out) != list:
    self.out = []
  self.out.append(val)
  if val < 256:
    print(chr(val), end="")

class Machine:
 
  def __init__(self, prog, inp=None, out=None, name=None):
    if type(prog) == str:
      prog = load_program(prog)
    self.inplen = len(prog)
    self.prog = defaultdict(int)
    for i in range(0, len(prog)):
      self.prog[i] = prog[i]
    if inp == None:
      inp = []
    self.inp = inp
    self.inpfun = default_inpfun if type(inp) == list or type(inp) == str else inp
    if out == None:
      out = []
    self.out = out 
    self.outfun = default_outfun if type(out) == list else out
    self.name = name if name else ""
    self.pc = 0
    self.inp_ptr = 0
    self.waiting = False
    self.halted = False
    self.rel_base = 0

  def step(self):
    if self.halted: 
      return



    prog = self.prog
    pc = self.pc
    
    #print(str(pc) + ", ", end = "")

    instr = prog[pc]
    op = instr%100

    if op == 1:
      self.arith_op(lambda x, y: x+y)
    elif op == 2:
      self.arith_op(lambda x, y: x*y)
    elif op == 3:
      val = self.inpfun(self)
      if val == "wait":
        self.waiting = True
        return
      else:
        if type(val) == str:
          val = ord(val)
        prog[self.indr_write(1)] = val
        self.waiting = False
    elif op == 4:
      self.outfun(self, self.indr(1))
      
    elif op == 5:
      if self.indr(1) != 0:
        self.pc = self.indr(2) 
        return
    elif op == 6:
      if self.indr(1) == 0:
        self.pc = self.indr(2) 
        return
    elif op == 7:
      self.arith_op(lambda x, y: int(x<y))
    elif op == 8:
      self.arith_op(lambda x, y: int(x==y))
    elif op == 9:
      self.rel_base += self.indr(1)
    elif op == 99:
      self.halted = True
      return

    else:
      self.debug()
      raise Exception("bad opcode " + str(op) + " at " + str(pc))

    self.pc = pc + op_lens[op]  

  def run(self, debugging=False, ascii=False):
    while not self.halted:
      self.step()
      if debugging:
        self.debug()
      if self.waiting and self.inpfun == default_inpfun:
        self.debug()
        raise "Ran out of input!"
    return self.out if not ascii else ''.join([chr(c) for c in self.out if c < 256])

  def run_until_input(self, ascii=False):
    out_ptr = len(self.out)
    self.step()
    while not (self.halted or self.waiting):
      #print(self.pc)
      self.step()
    ret = self.out[out_ptr:]
    return ret if not ascii else ''.join([chr(c) for c in ret if c < 256])

  def send_input(self, inp):
    if type(inp) == list:
      self.inp += inp
    elif type(inp) == str:
      if type(self.inp) == str:
        self.inp += inp
      else:
        self.inp += [ord(c) for c in inp]
    elif type(inp) == int:
      self.inp.append(inp)
    else:
      raise "Unexpected input type!"

  def indr(self, off):
    prog, pos = self.prog, self.pc
    mode = param(prog[pos], off)
    if mode == 1:
      return prog[pos+off]
    elif mode == 2:
      return prog[prog[pos+off]+self.rel_base]
    else:
      return prog[prog[pos+off]]

  def indr_write(self, off):
    prog, pos = self.prog, self.pc
    mode = param(prog[pos], off)
    if mode == 2:
      return prog[pos+off]+self.rel_base
    else:
      return prog[pos+off]

  def arith_op(self, f):
    prog, pc = self.prog, self.pc
    prog[self.indr_write(3)] = f(self.indr(1), self.indr(2))

  def debug(self):
    (prog, pc) = (self.prog, self.pc)
    if self.name != "":
      print("Machine name: " + self.name)
    print("Program Counter: " + str(self.pc))
    print("Current Opcode: " + str(prog[pc]))
    print("Rel Base: " + str(self.rel_base))

    i = 0
    while i < self.inplen or i < self.pc+6:
      op = prog[i]%100
      leng = op_lens[op] if op in op_lens else 1
      print("[" + str(i) + "] ", end = "")
      for j in range(0, leng):
        print(str(prog[i+j]) + ", ", end="")
      print(" <=========== " if i == pc else "")
      i+=leng
    print(prog[i])
    
    print()
    print()

def param(instr, off): 
  return instr//(10**(off+1)) %10



