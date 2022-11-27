from intcode import *
from utils import *

mach = Machine(None, ascii_input, ascii_output)

mach.run()

print()
print()
print(mach.out[-1])

"""
Part 1:
NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
WALK

Part 2:
NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
NOT E T
NOT T T
OR H T
AND T J
RUN
"""
