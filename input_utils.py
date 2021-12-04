import os
from datetime import datetime
from time import sleep

from misc_utils import ints_in


def readlines(filename: str) -> list[str]:
    """
    Returns the list of lines in the given file. Strips the trailing newline on each.
    """
    return [l[:-1] if l[-1] == '\n' else l for l in open(filename_for(filename))]


def groups(filename: str) -> list[str]:
    """
    Splits the contets of the given file into groups separated by two newlines. 
    Strips whitespace around each group, such as trailing newlines.
    """
    return [gr.strip() for gr in open(filename_for(filename)).read().split("\n\n")]


def submit(answer: int, part=1, day=None, year=2021, confirm=True) -> None:
    """
    Submits the answer to the AOC server, then exits. Asks for confirmation first if confrm is set.
    Use with caution, as an incorrect answer will lock you out for a minute.
    """
    if confirm:
        print(f"Submit {answer} to part {part}? (y/n)")
        if input()[0] != "y":
            return

    cmd = f"./submit {part} {answer}"
    if(day):
        cmd += f" {str(day)} {str(year)}"
    os.system(cmd)
    exit()


def filename_for(f):
    """
    If input is a string, returns it' if it's an integer then returns the filename for its input file.
    """
    if isinstance(f, str):
        return f
    else:
        return f"{f}.in"


def get_input(day=None, year=2021, filename=None, verbose=True):
    """
    Downloads and returns the input, as a list of lines; or a list of ints if every line is an int. 
    Defaults to today. 
    If verbose is true, prints some stats.
    """
    def printv(s):
        if verbose:
            print(s)

    def numeric(s):
        if len(s) > 1 and s[0] == "0":
            return False
        try:
            int(s)
            return True
        except ValueError:
            return False

    def csv_numeric(s):
        return all(numeric(x) for x in s.split(","))

    now = datetime.now()

    if day == None:
        day = now.day

    waited = False

    if (now.day, now.month, now.year) == (day, 12, year) and now.hour < 5:
        unlock = now.replace(hour=5, minute=0, second=1)
        diff = (unlock-now).total_seconds()
        printv(f"Waiting {diff} seconds")
        sleep(diff)

    filename = filename_for(day)
    if not os.path.isfile(filename) or open(filename).read().strip() == "" or waited:
        printv(f"Downloading input for {year} day {day} to {filename}")
        os.system(f"bash -c './aocfetch {day} {year} > {filename}'")
    else:
        printv(f"Using cached input from {filename}")

    inp = readlines(filename)

    if verbose:
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

    if all(numeric(l) for l in inp):
        return [int(l) for l in inp]

    return inp
