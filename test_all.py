#! /usr/bin/env python3

import sys
import os


def print_usage():
    print("""
Usage: ./test_all.py [year] [part]
Tests all days in the given year, or all years, using autotest.py.
""")


if "--help" in sys.argv or "-h" in sys.argv:
    print_usage()
    exit(0)

years = list(range(2018, 2023))
argv = sys.argv[1:]
part = 2

try:
    if len(argv) == 2:
        year, part = argv[:2]
        year = int(year)
        part = int(part)
        assert (year >= 2015)
        assert part in [1, 2]
        years = [year]
    elif len(argv) == 1:
        x = int(argv[0])
        if x in [1, 2]:
            part = x
        elif x >= 2015:
            year = x
        else:
            assert False
except (ValueError, AssertionError):
    print_usage()
    exit(1)

manual_input = [(2019, 8), (2019, 11), (2019, 21), (2019, 25), (2021, 13), (2022, 10)]

curdir = os.path.dirname(sys.argv[0])

no_p1 = [(2019, 24), (2020, 11), (2021, 23)]

success = 0
fail = []
for year in years:
    for day in range(1, 26):
        if (year, day) in manual_input:
            continue
        if part == 1 and ((year, day) in no_p1 or day == 25):
            continue
        if os.path.exists(f"{curdir}/{year}/{day}/sol.py"):
            print(f"\n======== Testing year {year} day {day} ========\n")
            if os.system(f"{curdir}/autotest.py {year} {day} {part}"):
                fail.append((year, day))
            else:
                success += 1

print("\n\n==========================================\n\n")
print(f"{success} days passed; {fail} failed")
exit(len(fail))
