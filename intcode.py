from collections import defaultdict
from input_utils import input_filename
# TODO: Find a way to have this be in the 2019 folder

"""
Intcode virtual machine

Brief Intcode spec, see aoc 2019 for further details:

A program is a list of integers.
There are 10 opcodes:
1 b b a: addition
2 b b a: multiplication
3 a: input
4 b: output
5 b b: jump (to second arg) if nonzero
6 l b: jump (to second arg) if zero
7 b b a: less than
8 b b a: equal to
9 b: adjust the relative base
99: halt

a = output operand (output is written to this address); b = input operand.
There are 3 addressing modes, determined by the upper digits of the opcode:
0: direct
1: immediate (not used for writes)
2: relative indirect
"""


def load_program(file=None):
    """
    Loads an intcode program from a file.
    """
    if file is None:
        file = input_filename()
    with open(file) as f:
        return list(map(int, f.read().split(",")))


# The lengths of each opcode.
op_lens = {1: 4, 2: 4, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 2}


def default_inpfun(self):
    """
    The default input function. 
    It will simply read from its input buffer and wait when it's empty.
    """
    if len(self.inp) <= self.inp_ptr:
        return "wait"
    else:
        # don't input.pop(0) because day 7 requires knowing the last output
        val = self.inp[self.inp_ptr]
        self.inp_ptr += 1
        return val


def default_outfun(self, val):
    """
    The default output function.
    It will simply write to its output buffer
    """
    self.out.append(val)


def ascii_input(self):
    """
    An input function that prompts the user for an ascii string.
    """
    if len(self.inp) == 0:
        self.inp = [ord(c) for c in input()+'\n']
    val = self.inp.pop(0)
    return val


def ascii_output(self, val):
    """
    An output function that prints the output to the screen as ascii.
    """
    if type(self.out) != list:
        self.out = []
    self.out.append(val)
    if val < 256:
        print(chr(val), end="")


class Machine:
    """
    An intcode machine. It has a running program, and input/output buffers.

    The fields self.inp, self.out, and self.np_ptr determine the state of the I/O buffers while the machine is running.

    Arguments:
    - prog: The program, which is copied internally. (so it's safe to use one program to initialise multiple machines).
        If it's a string, it's treated as a filename to load the program from.
    - inp: If it's a list or string, set the input buffer accordingly. 
        The internal buffer will alias inp if it's a list.
        inp may also be a function that will be called when the machine needs to input.
        It should return an integer, character, or the string "wait". 
        When "wait" is returned, the self.waiting field of the machine is set.
    - out: If it's a list, the internal output buffer will alias it.
        If it's a function, it's called whenever the machine outputs. 
        It is responsible for appending to the output buffer if desired.
    - name: The name of the machine, printed in debug logs and stored in the name field.
    """

    def __init__(self, prog=None, inp=None, out=None, name=None):
        if type(prog) == str or prog is None:
            prog = load_program(prog)
        self.inplen = len(prog)
        self.prog = defaultdict(int)
        for i in range(0, len(prog)):
            self.prog[i] = prog[i]
        self.inp = inp if type(inp) == list else [ord(c) for c in inp] if type(inp) == str else []
        self.inpfun = default_inpfun if type(inp) == list or type(inp) == str or inp is None else inp
        self.out = out if type(out) == list else []
        self.outfun = default_outfun if out is None or type(out) == list else out
        self.name = name if name is not None else ""
        self.pc = 0
        self.inp_ptr = 0
        self.waiting = False
        self.halted = False
        self.rel_base = 0

    def step(self):
        """
        Runs the machine for one step.
        The fields waiting and halted are set to reflect the state of the machine.
        """
        if self.halted:
            return

        prog = self.prog
        pc = self.pc

        # print(str(pc) + ", ", end = "")

        instr = prog[pc]
        op = instr % 100

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
                prog[self.addr(1)] = val
                self.waiting = False
        elif op == 4:
            self.outfun(self, self.read(1))

        elif op == 5:
            if self.read(1) != 0:
                self.pc = self.read(2)
                return
        elif op == 6:
            if self.read(1) == 0:
                self.pc = self.read(2)
                return
        elif op == 7:
            self.arith_op(lambda x, y: int(x < y))
        elif op == 8:
            self.arith_op(lambda x, y: int(x == y))
        elif op == 9:
            self.rel_base += self.read(1)
        elif op == 99:
            self.halted = True
            return

        else:
            self.debug()
            raise Exception("bad opcode " + str(op) + " at " + str(pc))

        self.pc = pc + op_lens[op]

    def run(self, debugging=False, ascii=False):
        """
        Runs the machine to completion. Raises an error if it gets stuck waiting for input.

        Returns the contents of the output buffer. If the ascii flag is set, it's returned as a string.

        If the debugging flag is set, print debugging information.
        """
        while not self.halted:
            self.step()
            if debugging:
                self.debug()
            if self.waiting and self.inpfun == default_inpfun:
                self.debug()
                raise Exception("Ran out of input!")
        return self.out if not ascii else ''.join([chr(c) for c in self.out if c < 256])

    def run_until_input(self, ascii=False):
        """
        Runs the machine to completion or until it gets stuck waiting for input.

        Returns the contents of the output buffer. If the ascii flag is set, it's returned as a string.

        If the debugging flag is set, print debugging information.
        """
        out_ptr = len(self.out)
        self.step()
        while not (self.halted or self.waiting):
            # print(self.pc)
            self.step()
        ret = self.out[out_ptr:]
        return ret if not ascii else ''.join([chr(c) for c in ret if c < 256])

    def send_input(self, inp):
        """
        Appends inp to the input buffer. inp can be an int, a list of ints, or a string.
        """
        if type(inp) == list:
            self.inp += inp
        elif type(inp) == str:
            self.inp += [ord(c) for c in inp]
        elif type(inp) == int:
            self.inp.append(inp)
        else:
            raise Exception("Unexpected input type!")

    def read(self, off):
        """Reads the off'th operand of the current opcode, taking the addressing mode into account."""
        return self.prog[self.addr(off)]

    def addr(self, off):
        """The address to read from or write to to handle the off'th operand of the current opcode"""
        prog, pos = self.prog, self.pc
        mode = getmode(prog[pos], off)
        if mode == 1:
            return pos+off
        if mode == 2:
            return prog[pos+off]+self.rel_base
        else:
            return prog[pos+off]

    def arith_op(self, f):
        """Common implementation of the binary arithmetic opcodes"""
        prog, _ = self.prog, self.pc
        prog[self.addr(3)] = f(self.read(1), self.read(2))

    def debug(self):
        """ Prints debug info """
        (prog, pc) = (self.prog, self.pc)
        if self.name != "":
            print("Machine name: " + self.name)
        print("Program Counter: " + str(self.pc))
        print("Current Opcode: " + str(prog[pc]))
        print("Rel Base: " + str(self.rel_base))

        i = 0
        while i < self.inplen or i < self.pc+6:
            op = prog[i] % 100
            leng = op_lens[op] if op in op_lens else 1
            print("[" + str(i) + "] ", end="")
            for j in range(0, leng):
                print(str(prog[i+j]) + ", ", end="")
            print(" <=========== " if i == pc else "")
            i += leng
        print(prog[i])

        print()
        print()


def getmode(instr, off):
    """Computes the addressing mode for the off'th parameter of instr"""
    return instr//(10**(off+1)) % 10
