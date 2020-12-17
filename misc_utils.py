from collections import defaultdict
import math
import os
import re
from attrdict import AttrDict
from typing import Tuple, Callable, Iterable, Optional


block_char = '█'


def irange(*args) -> range:
    """Inclusive range"""
    args = list(args)
    if len(args) == 1:
        args[0] += 1
    else:
        args[1] += 1
    return range(*args)


def bounds(xs, key=None):
    """
    Returns the minimum and maximum of xs.
    """
    xs = list(xs)
    return (min(xs, key=key), max(xs, key=key))


def sign(x) -> int:
    """Returns the sign of x"""
    if x < 0:
        return -1
    if x > 0:
        return 1
    return 0


def egcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Performs the extended Euclidian algorithm.
    Returns (g, x, y) such that x*a + y*b = g, and g = gcd(a, b).
    """
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def mod_inv(a: int, m: int) -> int:
    """Returns the inverse of a modulo m"""
    g, x, _ = egcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist', a, m)
    else:
        return x % m


def crt(mods, vals=None):
    """
    Implements the Chinese Remainder Theorem to find the smallest X such that X % n_i = a_i for each applicable i.
    The n_i must be pairwise coprime.
    mods is either a dict {n_i:a_i}, a list [(n_i,a_i)], or a list [n_i] along with vals = [a_i]

    Implementation adapted from https://rosettacode.org/wiki/Chinese_remainder_theorem#Python
    """
    if vals != None:
        mods = zip(mods, vals)
    elif isinstance(mods, dict):
        mods = mods.items()

    sum = 0
    prod = math.prod([n for (n, i) in mods])
    for n_i, a_i in mods:
        p = prod // n_i
        sum += a_i * mod_inv(p, n_i) * p
    return sum % prod


def clear_screen() -> None:
    """Clears the screen of the terminal"""
    print(chr(27) + "[2J")


def mapl(f: Callable, *xs) -> list:
    """Like map but returns a list"""
    return list(map(f, *xs))


def ints(xs: list) -> list[int]:
    """Casts each element of xs to an int"""
    return mapl(int, xs)


def mint(x, default=None):
    """Maybe int - casts to int and returns default on failure"""
    try:
        return int(x)
    except ValueError:
        return default


def ints_in(x: str, allow_neg=False) -> list[int]:
    """Finds and parses all integers in the string x"""
    ex = r'-?\d+' if allow_neg else r'\d+'
    return ints(re.findall(ex, x))


def match(regex: str, text: str, exact=True, ints=True, onfail=None):
    """
    Matches the given regex against the given string, and returns the capture groups.
    If the match succeeds but there were no capture groups, returns True.
    Returns onfail if the match failed.
    exact determines whether the whole string must be matched, and ints determines whether to parse integers from the result.
    """
    f = re.fullmatch if exact else re.search
    m = f(regex, text)
    if not m:
        return onfail
    grs = list(m.groups())
    if len(grs) == 0:
        return True

    if ints:
        grs = [mint(x, x) for x in grs]

    return grs


def modify_idx(xs, i: int, v):
    """
    When xs is a list or tuple, return a new list or tuple with the item at index i being changed to v
    """
    if isinstance(xs, list):
        ty = list
    elif isinstance(xs, tuple):
        ty = tuple
    else:
        raise TypeError("Expected list or tuple", type(xs), xs)

    new = [x for x in xs]
    new[i] = v
    return ty(new)


def ident(x):
    """The identity function."""
    return x

#pylint: disable=unsubscriptable-object


def bin_search(lo: int, hi: Optional[int], f: Callable[[int], bool]):
    """
    Performs a binary search on an abstract search space.

    Arguments:
    - lo: The low endpoint.
    - hi: The high endpoint. Can be None to represent infinity.
    - f: A monotone-decreasing function int->bool; i.e. goes 11110000

    Returns:
    - The unique int target in the range [lo, hi) such that f = (lambda i: i <= target) on this range.
      In other words, the unique target such that f(target) and not f(target+1)

    Example:
    - If xs is a sorted list, bin_search(0, len(xs), lambda i: xs[i]<=n) returns the index of n in xs.
    """

    if (not (hi == None or lo < hi)):
        raise Exception("Empty range")

    if not f(lo):
        return lo

    if(hi == None):
        hi = lo*2 if lo > 0 else 32
        while(f(hi)):
            (lo, hi) = (hi, lo*2)

    # Invariant: lo <= target < hi; i.e. f(lo) and not f(hi)
    # This invariant is not completely checked at the start; since f might be undefined on hi.
    # However, it still holds if we assume f "would be" false beyond its range.

    while(hi - lo > 1):
        mid = (lo+hi)//2
        if f(mid):
            lo = mid
        else:
            hi = mid

    return lo


def readlines(filename: str) -> list[str]:
    """
    Returns the list of lines in the given file. Strips the trailing newline on each.
    """
    return [l[:-1] if l[-1] == '\n' else l for l in open(filename)]


def groups(filename: str) -> list[str]:
    """
    Splits the contets of the given file into groups separated by two newlines. 
    Strips whitespace around each group, such as trailing newlines.
    """
    return [gr.strip() for gr in open(filename).read().split("\n\n")]


def submit(answer: int, part=1, day=None, year=2020, confirm=True) -> None:
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
