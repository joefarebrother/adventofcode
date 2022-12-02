import os
import sys
from misc_utils import ints_in

is_ex = len(sys.argv) > 1 and "test" in sys.argv[1]


def printx(*args, **kwargs):
    """
    Prints only if running on example data
    """
    if is_ex:
        print(*args, *kwargs)


def inp_readlines() -> list[str]:
    """
    Returns the list of lines in the given file. Strips the trailing newline on each.
    """
    with open(input_filename()) as f:
        return [l[:-1] if l[-1] == '\n' else l for l in f]


def inp_readall() -> str:
    """
    Returns the contents of the given file as a string.
    """
    with open(input_filename()) as f:
        return f.read()


def inp_groups(split=True) -> list[str]:
    """
    Splits the contents of the given file into groups separated by two newlines.
    Strips whitespace around each group, such as trailing newlines.
    """
    res = [gr.strip() for gr in inp_readall().split("\n\n")]
    if not res[-1]:
        res = res[:-1]
    if split:
        res = [gr.splitlines() for gr in res]
    return res


def input_filename(argv_override=True):
    """
    Gets the filename of the input file.
    If argv_override is true, an sys.argv[1] exists, that is returned instead.
    """
    if argv_override and len(sys.argv) > 1:
        return sys.argv[1]
    curdir = os.path.dirname(sys.argv[0])
    return f"{curdir}/real.in"


def numeric(s, len_limit=False):
    if len(s) > 16 and len_limit:
        # aoc numbers are pretty much always below 2^53 (16 digits) to avoid precision errors with languages like JS that only offer floats.
        # So anything longer than that should be treated as a string of digits for the purpose of determining whether to auto-cast input.
        return False
    if len(s) > 1 and s[0] == "0":
        return False
    try:
        int(s)
        return True
    except ValueError:
        return False


def csv_numeric(s, len_limit=False):
    return "," in s and all(numeric(x, len_limit=len_limit) for x in s.split(","))


def print_input_stats(inp):
    if type(inp) == str:
        inp = inp.splitlines()
    print(f"Lines: {len(inp)}")
    print(f"Blank lines: {inp.count('')}")
    print(f"Numeric lines: {sum(numeric(l, len_limit=True) for l in inp)}")
    print(f"CSV Numeric lines: {sum(csv_numeric(l) for l in inp)}")
    if len(set(len(l) for l in inp)) == 1 and len(inp) != 1:
        print("Looks like a grid")

    nums = ints_in(" ".join(inp))
    nums = [n for n in nums if len(str(n)) <= 16]
    if nums:
        print(f"Min integer: {min(nums)}")
        print(f"Max integer: {max(nums)}")

    if len(inp) < 10 and all(len(l) < 100 for l in inp):
        for l in inp:
            print(l)
