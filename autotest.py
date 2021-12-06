#! /usr/bin/env python3.9

# Based on https://github.com/penteract/adventofcode/blob/master/autotest.py

import urllib.request as r
from datetime import datetime
import os
import sys
from input_utils import get_day_year, get_input, numeric, readlines

usage = """
Python script for advent of code which downloads the problem description,
attempts to extract sample input and corresponding output,
then runs day{n}.py (where n is the day) on the sample input whenever day{n}.py is modified until
day{n}.py gives the sample output. When it does, day{n}.py gets run on the real input
and if that succeeds, the last printed word gets submitted automatically.

call as `autotest.py {year} {day}` with the
environment variable $AOC_KEY set to the value of your session cookie

files used:
day{n}.py   This program assumes that your solution for the part you are
            currently working on is in this file.
            Run as `python3 sol.py {input}` where {input} is the name of
            a file from which sol.py is expected to read the input
            for the day's problem
            
{n}.in      Your personal input (https://adventofcode.com/{year}/day/{day}/input)

The following files are all stored in test/{year}/{day}
input1      the automatically extracted sample input
            By default this is the first non-inline code block.
            It may be wrong, and if so you must manually edit it and restart this
            program if you want it to work correctly.
            If no appropriate sample input is found, you must create this file
            to use this program.
            
output1-1   the automatically extracted sample output for part 1
            By default, this is the last highlighed thing at the end of a code tag.
            It may be wrong, and if so you must manually edit it and restart this
            program if you want it to work correctly.
            If no appropriate sample output is found, you must create this file
            to use this program.
            
output1-2   the automatically extracted sample output for part 2
page1.html  the page when solving part 1
page2.html  the page when solving part 2
wrong_ans   a text file containing a list of answers which have been rejected
            Hopefully avoids repeatedly submitting wrong answers
            Does not distinguish between part 1 and part 2
            
tmp         stores the output of the solution on sample input
            Can be deleted without consequence except while the solution is running
            
tmpreal     stores the output of the solution on the real input
            Can be deleted without consequence except while the solution is running
"""


sesh = os.environ["AOC_KEY"]
if not sesh:
    raise Exception("Environment variable AOC_KEY not set")

headers = {"Cookie": "session="+sesh}


def writeTo(file, content):
    with open(file, mode="w") as f:
        f.write(content)


def read_string(file):
    with open(file) as f:
        return f.read()


def get_or_save(url, file):
    if file is None or not os.path.isfile(file):
        print("requesting url", repr(url))
        r1 = r.urlopen(r.Request(url, headers=headers))
        s = "".join(l.decode() for l in r1)
        if file is not None:
            writeTo(file, s)
    else:
        s = read_string(file)
    return s


def submit(part, answer):
    global submittime
    url = f"https://adventofcode.com/{year}/day/{day}/answer"
    print(f"submitting", repr(answer), "to url", repr(url))
    resp = r.urlopen(r.Request(url, data=bytes(
        f"level={part}&answer={answer}", "utf8"), headers=headers))
    submittime = datetime.now()
    print("time", submittime)
    print("response:")
    prnt = False
    content = ""
    correct = False
    for line in resp:
        line = line.decode()
        if "<article>" in line:
            prnt = True
        if prnt:
            print(line, end="")
            content += line
        if "</article>" in line:
            prnt = False
    return resp, content


for arg in sys.argv[1:]:
    if "help" in arg or "-h" in arg:
        print(usage)
        exit(0)

year = sys.argv[1] if len(sys.argv) >= 2 else None
day = sys.argv[2] if len(sys.argv) >= 3 else None
day, year = get_day_year(day, year)

workdir = os.path.normpath(
    f"{os.path.dirname(sys.argv[0])}/test/{year}/{day}/")
os.makedirs(workdir, exist_ok=True)

dayurl = f"https://adventofcode.com/{year}/day/{day}"

input_file = f"{day}.in"
solution_file = f"{day}.py"
get_or_save(dayurl + "/input", f"{day}.in")


wrong_ans_file = workdir + "wrong_ans"
bad_answers = set()
if os.path.isfile(wrong_ans_file):
    with open(wrong_ans_file) as f:
        for line in f:
            bad_answers.add(line.strip())


def add_bad(ans):
    bad_answers.add(ans)
    with open(wrong_ans_file, mode="a") as f:
        print(ans, file=f)


def find_examples(part):
    if not os.path.isfile(workdir+"input1"):
        print("Trying to find sample input to save in ", workdir+"input1")
        s = get_or_save(dayurl, f"{workdir}/page{part}.html")

        start = s.find("<pre><code>")
        end = s.find("</code></pre>")
        assert start != -1  # can't find pre block
        assert end != -1  # can't find end of pre block !!!

        eg = s[start+len("<pre><code>"):end].replace("<em>",
                                                     "").replace("</em>", "")
        writeTo(workdir+"input1", eg)
        print("assumed input:")
        print(eg)
    outputfile = workdir+"output1-"+part
    if not os.path.isfile(outputfile):
        print("Trying to find sample output to save in ", outputfile)
        s = get_or_save(dayurl, f"page{part}.html")

        completed = s.count("Your puzzle answer was")
        if str(completed+1) != part:
            raise Exception(
                f"the given part ({part}) cannot be done when {completed} are completed")

        last = s.rfind("</em></code>")
        assert last != -1  # can't find sample output
        start = s.rfind("<em>", 0, last)+len("<em>")
        assert start >= len("<em>")  # can't find start of sample output !!!
        if part == "2" and start <= s.find("--- Part Two ---"):
            raise Exception("Can't find part 2 sample output")
        sampleout = s[start:last]
        writeTo(outputfile, sampleout)
    else:
        sampleout = read_string(outputfile).strip()
    print("assumed output:", sampleout)


def run_examples(part):
    print("==== trying sample input (10 second timeout)\n")
    p = os.system(
        f"timeout 10 python3 {solution_file} {workdir}/input1 | tee {workdir}/tmp")
    if p:
        print("=== Example did not terminate successfully")
        return False
    answers = read_string(workdir+"tmp").split()

    if len(answers) == 0:
        print("=== Example produced no output")
        return False

    ans = answers[-1]
    sampleout = read_string(workdir+"output1-"+part)

    if ans != sampleout:
        print(
            f"=== Example failed: Expected {sampleout}, got {ans}")
        return False

    return [ans]


def run_real():
    print("==== trying real input (no timeout)")
    p = os.system(
        f"python3 {solution_file} {input_file} | tee {workdir}/tmpreal")
    print("==== end of program output")
    if p:
        print("Did not terminate successfully on real input")
        return False
    answer = read_string(workdir+"tmpreal").split()
    if len(answer) < 1:
        print("No output produced")
        return False
    answer = answer[-1]
    return answer


def doPart(part=None):
    if part is None:
        s = get_or_save(dayurl, None)
        completed = s.count("Your puzzle answer was")
        if completed > 1:
            raise Exception("You've already done enough parts")
        part = str(completed+1)
        writeTo(f"{workdir}/page{part}.html", s)
    else:
        part = str(part)

    ns = 0
    while True:
        while ns == (ns := os.stat(solution_file).st_mtime_ns):
            if os.system(f"inotifywait -q {solution_file}"):
                raise Exception("inotifywait did not terminate cleanly")
        ns = os.stat(solution_file).st_mtime_ns

        example_answers = run_examples(part)

        if example_answers:
            answer = run_real()
            if not answer:
                continue
            # do some checks on answer
            if(len(answer) < 3):
                print(repr(answer), "looks too small. Not submitting")
            elif answer in example_answers:
                print(repr(answer),
                      "is the same as the example output. Not submitting")
            elif not numeric(answer, len_limit=False) and numeric(example_answers[0], len_limit=False):
                print(
                    repr(answer), "isn't numeric, whereas the example output is. Not submitting.")
            elif answer in bad_answers:
                print(repr(answer), "previously submitted and failed. Not submitting")
            else:
                if not bad_answers or input("Do you want to submit", repr(answer), "(y/n)?") == "y":
                    print("Submitting answer:", repr(answer))
                    resp, content = submit(part=part, answer=answer)
                    if "That's the right answer!" in content:
                        break
                    elif "That's not the right answer" in content:
                        add_bad(answer)
                    else:
                        print(
                            "did not recognise success or incorrect, may be timeout or blank input or already completed")

    return part


if doPart() == "1":
    doPart("2")
