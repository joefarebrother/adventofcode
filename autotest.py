#! /usr/bin/env python3.9

# Based on https://github.com/penteract/adventofcode/blob/master/autotest.py

import urllib.request as r
from datetime import date, datetime
import os
import sys
import re
from input_utils import get_day_year, wait_for_unlock, print_input_stats, numeric
from time import sleep

usage = """
Python script for advent of code which downloads the problem description,
attempts to extract sample input and corresponding output,
then runs day{n}.py (where n is the day) on the sample input whenever day{n}.py is modified until
day{n}.py gives the sample output. When it does, day{n}.py gets run on the real input
and if that succeeds, the last printed word gets submitted automatically.

Call as `autotest.py {year} {day} [{part}]`, `autotest.py {day}`, or `autotest.py`; with the
environment variable $AOC_KEY set to the value of your session cookie.

If part is given, only run for the given part.

If called with the current day as input (which is the default if year and day are ommited), before the puzzle 
unlocks at 5am GMT, waits until it unlocks. This assumes that the local timezone is GMT.

Files used:
day{n}.py   This program assumes that your solution for the part you are
            currently working on is in this file.
            Run as `python3.9 day{n}.py {input}` where {input} is the name of
            a file from which day{n}.py is expected to read the input
            for the day's problem
            
{n}.in      Your personal input (https://adventofcode.com/{year}/day/{day}/input)

The following files are all stored in test/{year}/{day}
input1      The automatically extracted sample input
            By default this is the first non-inline code block.
            It may be wrong, and if so you must manually edit it and restart this
            program if you want it to work correctly.
            If no appropriate sample input is found, the program will still run but will require confrmation before submitting results.
            
output1-1   The automatically extracted sample output for part 1
            By default, this is the last highlighed thing at the end of a code tag.
            It may be wrong, and if so you must manually edit it and restart this
            program if you want it to work correctly.
            If no appropriate sample output is found, the program will still run but will require confrmation before submitting results.
            
output1-2   The automatically extracted sample output for part 2

input{n}    Input file for additional examples. 
            Will not be created automatically, but will be run if created manually.
output{n}-1 Output file for additional examples for part 1. 
            Will not be created automatically, but will be run if created manually.
            If the contents are [NONE], the example will be run but the output will not be verified. 
            An answer with no verified example outputs will not be submitted without confirmation.
output{n}-2 Output file for additional examples for part 2.

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

for arg in sys.argv[1:]:
    if "help" in arg or "-h" in arg:
        print(usage)
        exit(0)

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
    if file is None or not os.path.isfile(file) or read_string(file).strip() == "":
        print("requesting url", repr(url))
        r1 = r.urlopen(r.Request(url, headers=headers))
        s = "".join(l.decode() for l in r1)
        if file is not None:
            writeTo(file, s)
    else:
        s = read_string(file)
    return s


def touch(fn):
    with open(fn, "a") as f:
        pass


year = sys.argv[1] if len(sys.argv) >= 3 else None
day = sys.argv[2] if len(sys.argv) >= 3 else (
    sys.argv[1] if len(sys.argv) >= 2 else None)
day, year = get_day_year(day, year)


curdir = os.path.dirname(sys.argv[0])
workdir = os.path.normpath(f"{curdir}/test/{year}/{day}")+"/"
os.makedirs(workdir, exist_ok=True)

dayurl = f"https://adventofcode.com/{year}/day/{day}"

real_inputfile = f"{curdir}/{year}/{day}.in"
solution_file = f"{curdir}/{year}/day{day}.py"

touch(real_inputfile)
touch(solution_file)

wait_for_unlock(day, year)

real_input = get_or_save(dayurl + "/input", real_inputfile).splitlines()
print_input_stats(real_input)
print()

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


def tags(tag, html, exact_start=False, exact_end=False, strip=True):
    # insert stackoverflow post about parsing html with regex here
    r = f"(?s){'^'*exact_start}<{tag}(?: [^>]*)?>(.*?)</{tag}>{'$'*exact_end}"
    if isinstance(html, str):
        res = re.findall(r, html)
    else:
        res = [c for h in html for c in re.findall(r, h)]
    return [c.strip() for c in res] if strip else res


def remove_tags(tag, html, exact_start=False, exact_end=False):
    r = f"(?s){'^'*exact_start}<{tag}(?: [^>]*)?>(.*?)</{tag}>{'$'*exact_end}"
    return re.sub(r, "", html)


def html_entities(s):
    return s.replace("&gt;", ">").replace(
        "&lt;", "<").replace("&amp;", "&")


def find_examples(part):
    inputfile = workdir+"input1"
    pagefile = f"{workdir}/page{part}.html"
    outputfile = workdir+"output1-"+part

    might_have_inline_ex = len(real_input) <= 2
    looked = False

    if not os.path.isfile(inputfile):
        print("Trying to find sample input to save in ", inputfile)
        s = get_or_save(dayurl, pagefile)
        looked = True

        eg = tags("code", tags("pre", s), True, True, False)
        if not eg:
            print("Could not find example (No <pre><code> tags)")
            writeTo(inputfile, "[NONE]")
        else:
            eg = eg[0]
            eg = eg.replace("<em>", "").replace("</em>", "")
            eg = html_entities(eg)
            writeTo(inputfile, eg)
            print("Assumed input:")
            print(eg)
    else:
        print("Assumed input:")
        print(read_string(inputfile))

    if not os.path.isfile(outputfile):
        print("Trying to find sample output to save in", outputfile)
        s = get_or_save(dayurl, pagefile)
        looked = True

        completed = s.count("Your puzzle answer was")
        if str(completed+1) != part:
            raise Exception(
                f"the given part ({part}) cannot be done when {completed} are completed")

        if part == "2":
            s = s[s.find("--- Part Two ---"):]

        # lists may contain other examples, but (usually) not the answer to the current example
        if might_have_inline_ex:
            s = remove_tags("li", s)
        s = remove_tags("pre", s)

        o = tags("em", tags("code", s), exact_end=True)
        if not o:
            print("Could not find example output (no <code><em> tag)")
            sampleout = "[NONE]"
            writeTo(outputfile, "[NONE]")
        else:
            sampleout = o[-1]
            writeTo(outputfile, sampleout)
    else:
        sampleout = read_string(outputfile).strip()
        if sampleout == "[NONE]":
            print("No output specified.")
    print("Assumed output:", sampleout)

    if might_have_inline_ex and looked:
        # find more inline examples
        s = get_or_save(dayurl, pagefile)
        if part == "2":
            s = s[s.find("--- Part Two ---"):]

        s = remove_tags("pre", s)

        uls = tags("ul", s)
        if uls:
            ul = uls[-1]
            o = tags("em", tags("code", s), exact_end=True)
            if o and o[-1]+"</em></code>" in ul:
                # last highlighted answer was in a ul tag; probably in inline example
                # 2018 day 8 part 2 is a counterexample
                lis = tags("li", ul)
                for li in lis:
                    codes = tags("code", li)
                    if len(codes) >= 2:
                        em = tags("em", codes, exact_end=True)
                        if em:
                            inp, out = codes[0], em[-1]
                            if "<" not in inp and "<" not in out:
                                inp = html_entities(inp)
                                out = html_entities(out)
                                if len(inp) >= 5:
                                    add_example(inp, out, part)


def add_example(inp, out, part):
    print(f"Adding inline example: `{inp}` -> `{out}`")
    files = os.listdir(workdir)
    n = 2
    while f"input{n}" in files and read_string(f"{workdir}/input{n}") != inp:
        n += 1

    inpfile = f"{workdir}/input{n}"
    outfile = f"{workdir}/output{n}-{part}"

    writeTo(inpfile, inp)
    writeTo(outfile, out)


def tee(cmd, file):
    return os.system(f"bash -c '{cmd} | tee {file}; exit ${{PIPESTATUS[0]}}'")


def run_examples(part):
    """
    Runs the examples.
    Returns (ans, extra_ans, all_passed)
    """

    good = []
    unk = []

    for f in sorted(os.listdir(workdir)):
        if f.startswith("input"):
            try:
                idx = int(f[len("input"):])
            except:
                continue
            inputfile = workdir+f
            outputfile = f"{workdir}/output{idx}-{part}"
            if os.path.isfile(outputfile):
                if read_string(inputfile).strip() == "[NONE]":
                    print(f"Example {idx} skipped: No input found")
                    continue
                ans, suc = run_example(inputfile, outputfile, idx)
                if suc == None:
                    unk.append(ans)
                elif suc:
                    good.append(ans)
                else:
                    unk.append(ans)
                    return good, unk, False
            else:
                print(
                    f"Example {idx} skipped: No expected output file found (use a file containing [NONE] to run anyway)")
    return good, unk, True


def run_example(inputfile, outputfile, idx):
    """
    Runs a single example.
    Returns (ans, succ) where ans is the answer given, and succ is True if the test passed, False if it didn't, and None if no expected output was found.
    """
    tmpfile = workdir+"tmp"

    print(f"==== Trying example {idx} (10 second timeout)\n")
    p = tee(
        f"timeout 10 python3.9 {solution_file} {inputfile}", tmpfile)
    if p:
        print(f"=== Example {idx} did not terminate successfully")
        return None, False
    answers = read_string(tmpfile).split()

    if len(answers) == 0:
        print(f"=== Example {idx} produced no output")
        return None, False

    ans = answers[-1]
    sampleout = read_string(outputfile).strip()
    if sampleout == "[NONE]":
        return ans, None

    if ans != sampleout:
        print(
            f"=== Example {idx} failed: Expected {sampleout}, got {ans}")
        return ans, False

    return ans, True


def run_real():
    tmpfile = workdir+"tmpreal"

    print("==== trying real input (no timeout)")
    p = tee(
        f"python3.9 {solution_file} {real_inputfile}", tmpfile)
    print("==== end of program output")
    if p:
        print("Did not terminate successfully on real input")
        return False
    answer = read_string(tmpfile).split()
    if len(answer) < 1:
        print("No output produced")
        return False
    answer = answer[-1]
    return answer


submittime = None
bad_submittime = None


def submit(part, answer):
    global submittime, bad_submittime
    url = f"https://adventofcode.com/{year}/day/{day}/answer"
    print(f"Submitting", repr(answer), "to url", repr(url))
    if bad_submittime != None:
        timeout = (datetime.now() - bad_submittime).total_seconds()
        if timeout < 60:
            print(f"Waiting {timeout} seconds")
            sleep(61-timeout)
            print("Done")

    resp = r.urlopen(r.Request(url, data=bytes(
        f"level={part}&answer={answer}", "utf8"), headers=headers))

    submittime = datetime.now()
    print("time", submittime)
    print("response:")
    resp = "".join(l.decode() for l in resp)
    content = tags("article", resp)[0]
    print(content)
    return resp, content


def doPart(part=None):
    global bad_submittime
    if part is None:
        s = get_or_save(dayurl, None)
        completed = s.count("Your puzzle answer was")
        if completed > 1:
            raise Exception("You've already done enough parts")
        part = str(completed+1)
        writeTo(f"{workdir}/page{part}.html", s)
    else:
        part = str(part)

    find_examples(part)

    ns = 0
    while True:
        while ns == (ns := os.stat(solution_file).st_mtime_ns):
            if os.system(f"inotifywait -q -e modify {solution_file}"):
                print("\ninotifywait inturrupted (or errored)")
                exit(1)
        ns = os.stat(solution_file).st_mtime_ns

        print()

        good_answers, unknown_answers, all_passed = run_examples(part)
        example_answers = good_answers + unknown_answers

        if all_passed:
            if not good_answers:
                print(
                    "No examples were verified, so the result will not be submitted without confirmation")

            answer = run_real()
            if not answer:
                continue

            print("Verified example answers: ", good_answers)
            print("Unverified example answers: ", unknown_answers)
            print("Real answer: ", answer)

            # do some checks on answer
            if(len(answer) < 3):
                print(repr(answer), "looks too small. Not submitting")
            elif answer in good_answers + unknown_answers:
                print(repr(answer),
                      "is the same as the example output. Not submitting")
            elif not numeric(answer, len_limit=False) and numeric(example_answers[0], len_limit=False):
                print(
                    repr(answer), "isn't numeric, whereas the example output is. Not submitting.")
            elif answer in bad_answers:
                print(repr(answer), "previously submitted and failed. Not submitting")
            else:
                print("")
                if (good_answers and not bad_answers) or input(f"Do you want to submit {repr(answer)} (y/n)?") == "y":
                    print("Submitting answer:", repr(answer))
                    resp, content = submit(part=part, answer=answer)
                    if "That's the right answer!" in content:
                        bad_submittime = None
                        break
                    elif "That's not the right answer" in content:
                        add_bad(answer)
                        bad_submittime = submittime
                    else:
                        print(
                            "\nDid not recognise success or incorrect, may be timeout or blank input or already completed")

    return part


if len(sys.argv) >= 4:
    doPart(sys.argv[3])
else:
    if doPart() == "1":
        doPart("2")
