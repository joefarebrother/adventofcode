#! /usr/bin/env python3

import sys
import os
import re


def print_usage():
    print("""
Usage: ./test_all.py year
Tests all days in the given year using autotest.py.
""")


if "--help" in sys.argv or "-h" in sys.argv:
    print_usage()
    exit(0)

try:
    year = int(sys.argv[1])
except:
    print_usage()
    exit(1)

manual_input = [(2021, 13)]

curdir = os.path.dirname(sys.argv[0])

success = 0
fail = []
for day in range(1, 26):
    if (year, day) in manual_input:
        continue
    if os.path.exists(f"{curdir}/{year}/{day}/sol.py"):
        print(f"\n======== Testing year {year} day {day} ========\n")
        if (os.system(f"{curdir}/autotest.py {year} {day}")):
            fail.append(day)
        else:
            success += 1

print("\n\n==========================================\n\n")
print(f"{success} days passed; {fail} failed")
