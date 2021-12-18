import os
import sys
from datetime import datetime
from time import sleep
import urllib.request as r

from misc_utils import ints_in

is_ex = len(sys.argv) > 1 and "test" in sys.argv[1]


def printx(*args, **kwargs):
    """
    Prints only if running on example data
    """
    if is_ex:
        print(*args, *kwargs)


def readlines(filename, argv_override=True) -> list[str]:
    """
    Returns the list of lines in the given file. Strips the trailing newline on each.
    """
    with open(filename_for(filename, argv_override)) as f:
        return [l[:-1] if l[-1] == '\n' else l for l in f]


def readall(filename, argv_override=True) -> str:
    """
    Returns the contents of the given file as a string.
    """
    with open(filename_for(filename, argv_override)) as f:
        return f.read()


def groups(filename) -> list[str]:
    """
    Splits the contets of the given file into groups separated by two newlines.
    Strips whitespace around each group, such as trailing newlines.
    """
    return [gr.strip() for gr in readall(filename).split("\n\n")]


def filename_for(f, argv_override=True):
    """
    Gets the filename of the input file specified by f.
    If f is a string, raturns that relative to the directory the solution is in (i.e. sys.argv[0])
    If f is an int n, returns {n}.in relative to there
    If argv_override is true, an sys.argv[1] exists, that is returned instead and f is ignored.
    """
    if argv_override and len(sys.argv) > 1:
        return sys.argv[1]
    curdir = os.path.dirname(sys.argv[0])
    if isinstance(f, str):
        return os.path.join(curdir, f)
    else:
        return f"{curdir}/{f}.in"


def get_day_year(day=None, year=None):
    """
    If day or year are none and it's december, set them according to the corrent date and return them.
    """
    now = datetime.now()

    if not (day and year) and now.month != 12:
        raise Exception("Not december so could not determine intended date")

    if day == None:
        day = now.day
    if year == None:
        year = now.year

    return int(day), int(year)


def wait_for_unlock(day, year):
    now = datetime.now()
    if (now.day, now.month, now.year) == (day, 12, year) and now.hour < 5:
        unlock = now.replace(hour=5, minute=0, second=1)
        diff = (unlock-now).total_seconds()
        print(f"Waiting {diff} seconds")
        sleep(diff)


def numeric(s, len_limit=False):
    if len(s) > 1 and (len(s) <= 16 or not len_limit) and s[0] == "0":
        # aoc numbers are pretty much always below 2^53 (16 digits) to avoid precision errors with ;anguages like JS that only offer floats.
        # So anything longer than that should be treated as a string of digits for the pirpose of determining whether to auto-cast input.
        return False
    try:
        int(s)
        return True
    except ValueError:
        return False


def csv_numeric(s):
    return "," in s and all(numeric(x) for x in s.split(","))


def get_input(day=None, year=None, filename=None, verbose=True, convert_ints=True):
    """
    Downloads and returns the input, as a list of lines.
    If verbose is true, prints some stats.
    If convert_ints is true and every line is an numeric, casts them to integers.
    """
    def printv(s):
        if verbose:
            print(s)

    day, year = get_day_year(day, year)

    wait_for_unlock(day, year)

    if not filename:
        filename = filename_for(day, argv_override=False)
    if not os.path.isfile(filename) or readall(filename, argv_override=False).strip() == "":
        printv(f"Downloading input to {filename}")
        os.system(f"bash -c './aocfetch > {filename}")
    else:
        printv(f"Using cached input from {filename}")

    inp = readlines(filename, argv_override=False)

    if verbose:
        print_input_stats(inp)

    if convert_ints and all(numeric(l, True) for l in inp):
        return [int(l) for l in inp]

    return inp


def print_input_stats(inp):
    print(f"Lines: {len(inp)}")
    print(f"Blank lines: {inp.count('')}")
    print(f"Numeric lines: {sum(numeric(l) for l in inp)}")
    print(f"CSV Numeric lines: {sum(csv_numeric(l) for l in inp)}")
    if len(set(len(l) for l in inp)) == 1 and len(inp) != 1:
        print("Looks like a grid")

    nums = ints_in(" ".join(inp))
    if nums:
        print(f"Min integer: {min(nums)}")
        print(f"Max integer: {max(nums)}")

    if len(inp) < 10 and all(len(l) < 100 for l in inp):
        for l in inp:
            print(l)
