mode_pos = 0
mode_imm = 1
mode_rel = 2
DUMMY=0

def flatten(xss):
  return [x for xs in xss for x in xs]

def opcode(op, mode1=0, mode2=0, mode3=0):
  return op + 100*mode1 + 1000*mode2 + 10000*mode3

def add(a, b, res, a_mode = 1, b_mode = 1, res_mode = 0):
  return [opcode(1, a_mode, b_mode, res_mode), a, b, res]

def mul(a, b, res, a_mode = 1, b_mode = 1, res_mode = 0):
  return [opcode(2, a_mode, b_mode, res_mode), a, b, res]

def inp(res, mode=0):
  return [opcode(3, mode), res]

def out(a, mode=1):
  return [opcode(4, mode), a]

def jnz(a, lab, a_mode=1, lab_mode=1):
  return [opcode(5, a_mode, lab_mode), a, lab]

jtrue = jnz

def jz(a, lab, a_mode=1, lab_mode=1):
  return [opcode(6, a_mode, lab_mode), a, lab]

jfalse = jz

def tlt(a, b, res, a_mode = 1, b_mode = 1, res_mode = 0):
  return [opcode(7, a_mode, b_mode, res_mode), a, b, res]

def teq(a, b, res, a_mode = 1, b_mode = 1, res_mode = 0):
  return [opcode(8, a_mode, b_mode, res_mode), a, b, res]

def add_rel(a, mode = 1):
  return [opcode(9, mode), a]

def halt(): 
  return [99]

label_idx = 0
def fresh_lab(name="lab"):
  global label_idx
  label_idx += 1
  return name + str(label_idx)

def lab_def(lab):
  return [lab + ":"]

def remove_labels(code):
  labels = {}
  i = 0
  for instr in code:
    if type(instr) == str and instr[-1] == ":":
      labels[instr[:-1]] = i
    else:
      i+=1
  res = []
  for instr in code:
    if type(instr) == str:
      if not instr[-1] == ":":
        spl = instr.split("+")
        res.append(labels[spl[0]] + sum([int(j) for j in spl[1:]]))
    else:
      res.append(instr)
  return res

def register(name, init=0):
  return flatten([
    lab_def(name),
    add(init, 0, DUMMY),
    jz(0, DUMMY)
  ])

def read_reg_to(reg_name, res):
  lab = fresh_lab("read_"+reg_name)
  return flatten([
    add(res, 0, reg_name+"+3"),
    add(0, lab, reg_name+"+6"),
    jz(0, reg_name),
    lab_def(lab)
  ])  

def write_reg(val, reg_name):
  return add(val, 0, reg_name+"+1")

def call(sub):
  lab = fresh_lab(sub)
  return flatten([
    add(lab, 0, sub +"_end+2"),
    jz(0, sub +"_start"),
    lab_def(lab)
  ])

def write_mem_cell(real_defn=False):
  if real_defn:
    template = register("")[1:]
    template[3] = "mem_val+1"
    res = ["write_mem_cell_start:"]
    for off, instr in enumerate(template):
      if off == 1:
        continue # don't overrite the actual value
      lab = fresh_lab("write_mem")
      res += flatten([
        read_reg_to("mem_ptr", lab+"+1"),
        lab_def(lab),
        add(DUMMY, off, lab+"+7"),
        add(instr, 0, DUMMY)
      ])
    return flatten([
      res,
      ["write_mem_cell_end:"],
      jz(0, DUMMY)
    ])
  else:
    return call("write_mem_cell")


def write_mem(real_defn=False):
  if real_defn:   
    lab1 = fresh_lab("write_mem")
    lab2 = fresh_lab("write_mem")
    return flatten([
      ["write_mem_start:"],
      read_reg_to("mem_ptr", lab1+"+1"),
      lab_def(lab1),
      add(DUMMY, 1, lab2+"+3"),
      read_reg_to("mem_val", lab2+"+1"),
      lab_def(lab2),
      add(DUMMY, 0, DUMMY),
      ["write_mem_end:"],
      jz(0, DUMMY)
    ])
    return res
  else:
    return call("write_mem")

def read_mem(real_defn=False):
  if real_defn:
    lab1 = fresh_lab("read_mem")
    lab2 = fresh_lab("read_mem")
    lab3 = fresh_lab("read_mem")
    return flatten([
      ["read_mem_start:"],
      read_reg_to("mem_ptr", lab1+"+1"),
      read_reg_to("mem_ptr", lab2+"+6"),
      lab_def(lab1),
      add(DUMMY, 6, lab2+"+3"),
      lab_def(lab2),
      add(0, lab3, DUMMY),
      jz(0, DUMMY),
      lab_def(lab3),
      ["read_mem_end:"],
      jz(0, DUMMY)
    ])
  else:
    return call("read_mem")

    
def bf_incr():
  lab = fresh_lab("incr")
  return flatten([
    read_mem(),
    read_reg_to("mem_val", lab+"+1"),
    lab_def(lab),
    add(DUMMY, 1, lab+"+5"),
    write_reg(DUMMY, "mem_val"),
    write_mem()
  ])  

def bf_decr():
  lab = fresh_lab("decr")
  return flatten([
    read_mem(),
    read_reg_to("mem_val", lab+"+1"),
    lab_def(lab),
    add(DUMMY, -1, lab+"+5"),
    write_reg(DUMMY, "mem_val"),
    write_mem()
  ]) 

def bf_left():
  lab = fresh_lab("left")
  return flatten([
    read_reg_to("mem_ptr", lab+"+1"),
    lab_def(lab), 
    add(DUMMY, -(len(register(""))-1), lab+"+5"),
    write_reg(DUMMY, "mem_ptr")
  ])

def bf_right():
  lab = fresh_lab("right")
  return flatten([
    read_reg_to("mem_ptr", lab+"+1"),
    lab_def(lab), 
    add(DUMMY, len(register(""))-1, lab+"+5"),
    write_reg(DUMMY, "mem_ptr"),
    write_mem_cell()
  ])

def bf_inp():
  lab = fresh_lab("inp")
  return flatten([
    inp(lab+"+1"),
    lab_def(lab),
    write_reg(DUMMY, "mem_val"),
    write_mem()
  ])

def bf_out():
  lab = fresh_lab("out")
  return flatten([
    read_mem(),
    read_reg_to("mem_val", lab+"+1"),
    lab_def(lab),
    out(DUMMY)
  ])

def bf_loop_start(loop_lab):
  lab = fresh_lab("loop")
  return flatten([
    lab_def(loop_lab+"_start"),
    read_mem(),
    read_reg_to("mem_val", lab+"+1"),
    lab_def(lab),
    jz(DUMMY, loop_lab+"_end")
  ])

def bf_loop_end(loop_lab):
  return flatten([
    jz(0, loop_lab+"_start"),
    lab_def(loop_lab+"_end")
  ])

def compile(prog):
  code = flatten([
    jz(0, "defns"),
    register("mem_ptr", "mem_start"),
    register("mem_val"),
    write_mem_cell(True),
    write_mem(True),
    read_mem(True),
    lab_def("defns"),
    write_mem_cell()
  ])

  loop_stack = []
  for instr in list(prog):
    if instr == "+":
      code += bf_incr()
    elif instr == "-":
      code += bf_decr()
    elif instr == "<":
      code += bf_left()
    elif instr == ">":
      code += bf_right()
    elif instr == ",":
      code += bf_inp()
    elif instr == ".":
      code += bf_out()
    elif instr == "[":
      lab = fresh_lab("loop_body")
      loop_stack.append(lab)
      code += bf_loop_start(lab)
    elif instr == "]":
      lab = loop_stack[-1]
      loop_stack = loop_stack[:-1]
      code += bf_loop_end(lab)

  code += [99, "mem_start:"]

  return remove_labels(code)


prog = ",>,<[->+<]>."
iprog = compile(prog)

print(iprog)

from intcode import Machine

print(Machine(iprog, [5, 6]).run())









