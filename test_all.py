#! /usr/bin/env python3

import sys
import os


def print_usage():
    print("""
Usage: ./test_all.py [year]
Tests all days in the given year, or all years, using autotest.py.
""")


if "--help" in sys.argv or "-h" in sys.argv:
    print_usage()
    exit(0)

years = [2019, 2020, 2021]
if len(sys.argv) >= 2:
    try:
        years = [int(sys.argv[1])]
    except (ValueError):
        print_usage()
        exit(1)

manual_input = [(2021, 13), (2019, 8), (2019, 11), (2019, 21), (2019, 25)]

curdir = os.path.dirname(sys.argv[0])

success = 0
fail = []
for year in years:
    for day in range(1, 26):
        if (year, day) in manual_input:
            continue
        if os.path.exists(f"{curdir}/{year}/{day}/sol.py"):
            print(f"\n======== Testing year {year} day {day} ========\n")
            if (os.system(f"{curdir}/autotest.py {year} {day}")):
                fail.append((year, day))
            else:
                success += 1

print("\n\n==========================================\n\n")
print(f"{success} days passed; {fail} failed")
exit(len(fail))
