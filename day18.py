# pylint: disable=unused-wildcard-import
from utils import *

lines = readlines("18.in")


# class Tree:
#     def __init__(self, left, op, right):
#         self.left = left
#         self.right = right
#         self.op = op

#     def eval(self):
#         l = self.left if type(self.left) == int else self.left.eval()
#         r = self.right if type(self.right) == int else self.right.eval()
#         return l+r if self.op == "+" else l*r


# def parse(line, off=0):
#     off = strip_ws(line, off)
#     left, off = parse_operand(line, off)
#     off = strip_ws(line, off)
#     if off == len(line) or line[off] == "(":
#         return left, off
#     op, off = parse_op(line, off)
#     right, off = parse(line, off)
#     return Tree(left, op, right), off


# def strip_ws(line, off):
#     while off < len(line) and line[off].isspace():
#         off += 1
#     return off


# def parse_operand(line, off):
#     off = strip_ws(line, off)
#     if line[off] == ")":
#         res, off = parse(line, off+1)
#         return res, off+1
#     else:
#         print(line, "; off=", off, ";", line[off:])
#         res = ""
#         while off < len(line) and line[off].isdigit():
#             res += line[off]
#             off += 1
#         return int("".join(reversed(res))), off


# def parse_op(line, off):
#     off = strip_ws(line, off)
#     res = line[off]
#     off += 1
#     return res, off

class Num:
    def __init__(self, num):
        self.num = num

    def __add__(self, other):
        return Num(self.num * other.num)

    def __sub__(self, other):
        return Num(self.num + other.num)

    def __mul__(self, other):
        return Num(self.num + other.num)


tab = str.maketrans("+*", "*+")  # part 1: tab = str.maketrans("+*", "-+")


def process(line):
    tr = str.translate(line, tab)
    return re.sub(r'(\d+)', r'Num(\1)', tr)


pr = mapl(process, lines)
print(pr)
res = mapl(lambda l: eval(l).num, pr)
print(sum(res))
