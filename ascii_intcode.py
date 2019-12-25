from intcode import *
from sys import argv

if len(argv) != 2 or argv[1] == "--help":
  print("Usage: python ascii_intcode.py [intcode file]")
  exit()

Machine(argv[1], ascii_input, ascii_output).run()
