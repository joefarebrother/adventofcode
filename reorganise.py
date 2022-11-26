import os
import sys
import shutil
import re

"""Single-use script for reorganising my system"""

curdir = curdir = os.path.dirname(sys.argv[0])


def move_if_able(src, dest):
    if os.path.isfile(src):
        shutil.move(src, dest)


for year in range(2017, 2022):
    for day in range(1, 26):
        daydir = f"{curdir}/{year}/{day}"
        os.makedirs(daydir)
        move_if_able(f"{curdir}/{year}/day{day}.py", f"{daydir}/sol.py")
        move_if_able(f"{curdir}/{year}/{day}.in", f"{daydir}/real.in")
        testdir = f"{curdir}/test/{year}/{day}"
        if os.path.isdir(testdir):
            for f in os.listdir(testdir):
                m = re.fullmatch(r'input(\d+)', f)
                if m:
                    idx = m.groups(1)[0]
                    shutil.move(f"{testdir}/{f}", f"{daydir}/test{idx}.in")
                else:
                    m = re.fullmatch(r'output(\d+)-(\d)', f)
                    if m:
                        idx, part = m.groups(1)
                        shutil.move(f"{testdir}/{f}",
                                    f"{daydir}/test{idx}-part{part}.out")
                    else:
                        shutil.move(f"{testdir}/{f}", f"{daydir}/{f}")
