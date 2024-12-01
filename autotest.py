#! /usr/bin/env python3

# Based on https://github.com/penteract/adventofcode/blob/master/autotest.py

import urllib
import urllib.request as req
from datetime import datetime, timedelta
import os
import sys
import re
import platform
import math
from time import sleep
from input_utils import numeric, print_input_stats
from page_parts import PageParts

usage = """
Usage: ./autotest.py [year] [day] [part] [sol]

Python script for advent of code which downloads the problem description,
attempts to extract sample input and corresponding output,
then runs sol.py on the sample input whenever sol.py is modified until
sol.py gives the sample output. When it does, sol gets run on the real input
and if that succeeds, the last printed word gets submitted automatically.

Requires env var AOC_KEY to be the session cookie, which can be obtained from the browser.

If part is given, only run for the given part.
If sol is given, use that as the solution file rather than sol.py.
If year is not given, use the current year. If year and day are not given, use the current year and day, if it's December.

Some different orderings of the arguments are accepted, if it's unambiguous.

Files used, all under {year}/{day}:
sol.py      This program assumes that your solution for the part you are
            currently working on is in this file.
            Run as `python3 sol.py {input}` where {input} is the name of
            a file from which sol.py is expected to read the input
            for the day's problem

real.in      Your personal input (https://adventofcode.com/{year}/day/{day}/input)

test{n}.in  The input to test case {n}. 
            Test 1 is automatically extracted as the first code block that matches the real input, 
            and other inline tests may be extracted.
            Further tests can also be created manually.
            An empty file will be treated essentially as though it does not exist. 
            An input of [NONE] (written if no test was found) won't be run.
            A pair of empty input and output files are created automatically for convenience.

test{n}-part{p}.out   The expected output for test case {n}, part {p}.
                      The output to test case 1 is automatically extracted as the last emphasised code element.
                      An empty or non-existent output file will prevent the test case from being run at all for the given part.
                      An output of [NONE] will have its test case run but its output not be verified.


page{p}.html    the page when solving part {p}
pagefinal.html  the page after both parts have been solved.
wrong_ans{p}    a text file containing a list of answers which have been rejected for the given part, as well as whether they were too high or low.
                Hopefully avoids repeatedly submitting wrong answers

timeout     Overrides the default example timeout of 10 seconds

tmp         stores the output of the solution on sample input
            Can be deleted without consequence except while the solution is running

tmpreal     stores the output of the solution on the real input
            Can be deleted without consequence except while the solution is running
"""

if __name__ != "__main__":
    raise Exception("Don't import autotest")

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

for arg in sys.argv[1:]:
    if "help" in arg or "-h" in arg:
        print(usage)
        exit(0)

sesh = os.environ["AOC_KEY"]
if not sesh:
    raise Exception("Environment variable AOC_KEY not set")

headers = {"Cookie": "session="+sesh,
           "User-Agent": "autotest.py (https://github.com/joefarebrother/adventofcode by joseph.farebrother@gmail.com)"}


def write_to(file, content):
    with open(file, mode="w") as f:
        f.write(content)


def read_string(file):
    with open(file) as f:
        return f.read()


ratelimit_time = None


def ratelimit():
    global ratelimit_time
    if not (ratelimit_time is None or ratelimit_time < datetime.now()):
        diff = ratelimit_time-datetime.now()
        sleep(diff.total_seconds())
    ratelimit_time = datetime.now()+timedelta(seconds=1)


def get_or_save(url, file):
    if file is None or not os.path.isfile(file) or read_string(file).strip() == "":
        print("requesting url", repr(url))
        ratelimit()
        with req.urlopen(req.Request(url, headers=headers)) as resp:
            s = "".join(l.decode() for l in resp)
            if file is not None:
                write_to(file, s)
    else:
        s = read_string(file)
    return s


def touch(fn):
    with open(fn, "a"):
        pass


def wait_for_unlock(day, year):
    now = datetime.now()
    if (now.day, now.month, now.year) == (day, 12, year) and now.hour < 5:
        unlock = now.replace(hour=5, minute=0, second=1)
        diff = (unlock-now).total_seconds()
        print(f"Waiting {diff} seconds")
        sleep(diff)


def parse_args():
    argv = sys.argv[1:]
    year, day, part, sol = None, None, None, "sol"

    pot_sol = [s for s in argv if not numeric(s)]
    if len(pot_sol) > 1:
        print("Too many string arguments")
        exit(1)

    nums = [int(n) for n in argv if numeric(n)]
    pot_years = [n for n in nums if n >= 2015]
    pot_days = [n for n in nums if 1 <= n <= 25]

    if len(pot_years) > 1:
        print("Year ambiguous")
        exit(1)
    if len(pot_years) + len(pot_days) != len(nums):
        print("Numerical args found that aren't year or day")
        exit(1)
    if len(pot_days) > 2:
        print("Too many numerical args")
        exit(1)

    if pot_sol:
        sol = pot_sol[0]
    if pot_years:
        year = pot_years[0]
    if pot_days:
        day = pot_days[0]
        if len(pot_days) == 2:
            part = pot_days[1]
            if part not in [1, 2]:
                print(f"Invalid part {part}")
                exit(1)
            part = str(part)

    if year and not day:
        print("No day specified")
        exit(1)

    now = datetime.now()

    if not year:
        if now.month != 12:
            print("Not december, year and day required")
            exit(1)
        year = now.year
        if not day:
            day = now.day

    if (year, day) > (now.year, now.day):
        print("That time is in the future")
        exit(1)

    return year, day, part, sol


year, day, part_arg, sol_arg = parse_args()


curdir = os.path.dirname(sys.argv[0])
workdir = os.path.normpath(f"{curdir}/{year}/{day}")+"/"
os.makedirs(workdir, exist_ok=True)

dayurl = f"https://adventofcode.com/{year}/day/{day}"

real_inputfile = f"{workdir}/real.in"
solution_file = f"{workdir}/{sol_arg}.py"

completed = 0


class Wrong:
    def __init__(self, part):
        self.filename = f"{workdir}/wrong_ans{part}"
        self.answers = []
        self.toohigh = None
        self.toolow = None
        if os.path.isfile(self.filename):
            with open(self.filename) as f:
                for line in f:
                    ans = line.split()[0]
                    self.add_bad(ans, line, write=False)

    def add_bad(self, ans, content, write=True):
        self.answers.append(ans)
        extra = ""
        if "too high" in content:
            self.toohigh = min(int(ans), self.toohigh or math.inf)
            extra = " [too high]"
        if "too low" in content:
            self.toolow = max(int(ans), self.toolow or -math.inf)
            extra = " [too low]"
        if write:
            with open(self.filename, mode="a") as f:
                print(ans + extra, file=f)

    def is_toohigh(self, ans):
        if self.toohigh is None:
            return False
        return int(ans) >= self.toohigh

    def is_toolow(self, ans):
        if self.toolow is None:
            return False
        return int(ans) <= self.toolow


def summarize(s):
    if isinstance(s, list):
        s = '\n'.join(s)+'\n'
    s = re.sub(r'\d', '0', s)
    s = re.sub(r'[a-z]', 'a', s)
    s = re.sub(r'[A-Z]', 'A', s)
    return set(s)


def find_examples(part, page: PageParts):
    if year == 2019 and "intcode" in read_string(solution_file):
        return

    test1_inputfile = f"{workdir}/test1.in"
    test1_outputfile = f"{workdir}/test1-part{part}.out"

    might_have_inline_ex = len(real_input) <= 2
    looked = False

    if not os.path.isfile(test1_inputfile):
        print("Trying to find sample input to save in ", test1_inputfile)
        looked = True

        egs = page.possible_examples()
        if not egs:
            print("Could not find example (No <pre><code> tags)")
            write_to(test1_inputfile, "[NONE]")
        else:
            summarized_real = summarize(real_input)
            for i, eg in enumerate(egs):
                if summarize(eg) <= summarized_real:
                    write_to(test1_inputfile, eg)
                    print("Assumed input:")
                    print(eg)
                    break
                print(f"Code block {i} skipped; doesn't match input (contains {summarize(eg)-summarized_real})")
            else:
                print("Could not find example (No code block matches input)")
                write_to(test1_inputfile, "[NONE]")

    if not os.path.isfile(test1_outputfile):
        print("Trying to find sample output to save in", test1_outputfile)
        looked = True

        o = page.possible_outputs(part, no_li=True)
        if o:
            sample_out = o.last()
            write_to(test1_outputfile, sample_out)
        else:
            print("Could not find example output (no <code><em> tag)")
            sample_out = "[NONE]"
            write_to(test1_outputfile, "[NONE]")

    else:
        sample_out = read_string(test1_outputfile).strip()
        if sample_out in ["[NONE]", ""]:
            print("No output specified.")

    print("Assumed output:", sample_out)

    if might_have_inline_ex and looked:
        for inp, out in page.possible_inline_examples(part):
            add_example(inp, out, part)

    if looked:
        add_example("", "", part)


def add_example(inp, out, part):
    if inp and out:
        print(f"Adding inline example: `{inp}` -> `{out}`")
    files = os.listdir(workdir)
    n = 2
    while f"test{n}.in" in files and read_string(f"{workdir}/test{n}.in") != inp:
        n += 1

    inpfile = f"{workdir}/test{n}.in"
    outfile = f"{workdir}/test{n}-part{part}.out"

    write_to(inpfile, inp)
    write_to(outfile, out)


def tee(cmd, file):
    cmd = f"bash -c '{cmd} | tee {file}; exit ${{PIPESTATUS[0]}}'"
    return os.system(cmd)


def run_examples(part):
    """
    Runs the examples.
    Returns (ans, extra_ans, all_passed)
    """

    timeout = 10
    timeout_file = workdir + "timeout"
    if os.path.isfile(timeout_file):
        timeout = int(read_string(timeout_file))

    good = []
    unk = []

    for f in sorted(os.listdir(workdir)):
        m = re.fullmatch(r'test(\d+)\.in', f)
        if not m:
            continue

        try:
            idx = int(m.groups(1)[0])
        except ValueError:
            continue
        inputfile = workdir+f
        outputfile = f"{workdir}/test{idx}-part{part}.out"

        if not read_string(inputfile).strip():
            continue

        if not os.path.isfile(outputfile):
            print(f"Example {idx} skipped: No expected output file found (use a file containing [NONE] to run anyway)")
            continue

        if read_string(inputfile).strip() in "[NONE]":
            print(f"Example {idx} skipped: No input found")
            continue

        if read_string(outputfile).strip() == "":
            print(f"Example {idx} skipped: Output file empty")
            continue

        ans, suc = run_example(inputfile, outputfile, idx, part, timeout)
        if suc is None:
            unk.append(ans)
        elif suc:
            good.append(ans)
        else:
            unk.append(ans)
            return good, unk, False

    return good, unk, True


def run_example(inputfile, outputfile, idx, part, timeout):
    """
    Runs a single example.
    Returns (ans, succ) where ans is the answer given,
    and succ is True if the test passed, False if it didn't, and None if no expected output was found.
    """
    tmpfile = workdir+"tmp"

    print(f"==== Trying example {idx} ({timeout} second timeout)\n")
    p = tee(f"timeout --foreground {timeout} python3 -u {solution_file} {inputfile}", tmpfile)
    if p:
        print(f"=== Example {idx} did not terminate successfully")
        return None, False

    ans = answer_in_out(read_string(tmpfile), part)

    if ans is None:
        print(f"=== Example {idx} produced no output")
        return None, False

    sample_out = read_string(outputfile).strip()
    if sample_out == "[NONE]":
        return ans, None

    if ans != sample_out:
        print(f"=== Example {idx} failed: Expected {sample_out}, got {ans}")
        return ans, False

    return ans, True


def run_real(part):
    tmpfile = workdir+"tmpreal"

    print("==== trying real input (no timeout)")
    p = tee(f"python3 -u {solution_file} {real_inputfile}", tmpfile)
    print("==== end of program output")
    if p:
        print("Did not terminate successfully on real input")
        return False, None
    real_output = read_string(tmpfile)
    answer = answer_in_out(real_output, part)
    if answer == None:
        print("No output produced")
        return False, None
    if part == "2":
        p1answer = answer_in_out(real_output, "1")
        if p1answer != answer:
            return answer, p1answer
    return answer, None


def answer_in_out(out: list[str], part):
    out = out.splitlines()
    nout = []
    for o in out:
        if o.lower().startswith("part"):
            if o.lower().startswith(f"part {part}"):
                if o.lower().startswith("part 2") and part == "1":
                    return None
                o = o[len("part 1"):].strip(":").split()
                if o:
                    return o[-1].strip("()[]{}")
        else:
            nout.append(o)
    nout = " ".join(nout).split()
    if nout:
        if part == "1" and completed >= 1 and len(nout) == 2:
            nout = nout[0]
        else:
            nout = nout[-1]
        return nout.strip("()[]{}")
    return None


bad_submit_time = None


def submit(part, answer):
    global bad_submit_time
    url = f"https://adventofcode.com/{year}/day/{day}/answer"
    print(f"Submitting {answer} to url {url}")
    if bad_submit_time != None:
        timeout = (datetime.now() - bad_submit_time).total_seconds()
        if timeout < 60:
            print(f"Waiting {timeout} seconds")
            sleep(61-timeout)
            print("Done")

    ratelimit()
    with req.urlopen(req.Request(url, data=bytes(urllib.parse.urlencode({'level': part, 'answer': answer}), "utf8"), headers=headers)) as resp:

        submit_time = datetime.now()
        print("time", submit_time)
        print("response:")
        resp = "".join(l.decode() for l in resp)
        content = PageParts(resp).tags("article").last()
        print(content)

        passed = False
        failed = False
        if "That's the right answer!" in content:
            passed = True
            bad_submit_time = None
        if "That's not the right answer" in content:
            failed = True
            bad_submit_time = submit_time
        return content, passed, failed


def wait_for_changes(file):
    plat = platform.system()
    if plat == "Linux":
        if os.system(f"inotifywait -q -e modify {file}"):
            print("\ninotifywait interrupted (or errored)")
            exit(1)
    elif plat == "Darwin":  # mac
        tmpfile = workdir + "fswatchtmp"
        errcode = os.system(f"fswatch -1 {file} > {tmpfile}")
        if errcode or not read_string(tmpfile):
            print("\nfswatch interrupted (or errored)")
            exit(1)
    else:
        print(f"Why are you using {plat}?")
        exit(1)


def get_page(part):
    global completed

    final_file = workdir+"pagefinal.html"
    p2_file = workdir+"page2.html"
    if os.path.isfile(final_file):
        s = read_string(final_file)
    elif part == "1" and os.path.isfile(p2_file):
        s = read_string(p2_file)
    else:
        part_file = f"{workdir}/page{part}.html" if part else None
        s = get_or_save(dayurl, part_file)

    page = PageParts(s)
    correct_answers = list(page.tags("p").filter(lambda p: p.startswith("Your puzzle answer was")).tags("code"))
    
    completed = len(correct_answers)
    if "Both parts of this puzzle are complete" in s:
        completed = 2

    if completed == 2:
        write_to(final_file, s)
    if completed == 1:
        write_to(workdir+"page2.html", s)
    if completed == 0:
        write_to(workdir+"page1.html", s)
        if part == "2":
            raise Exception("Can't do part 2 without having completed part 1")

    return page, correct_answers


def answer_checks(answer: str, example_answers, correct_answers, wrong, part):
    """Does some checks on the given answer, returns True if they pass"""
    if len(answer) < 3:
        print(f"{answer} looks too small. Not submitting")
    elif any(ord(c) > 127 for c in answer):
        print(f"{answer} non-ascii. Not submitting.")
    elif answer in example_answers:
        print(f"{answer} is the same as the example output. Not submitting")
    elif not numeric(answer) and example_answers and numeric(example_answers[0]):
        print(f"{answer} isn't numeric, whereas the example output is. Not submitting.")
    elif part == "2" and correct_answers and answer == correct_answers[0]:
        print(f"{answer} is the same as the correct part 1 answer. Not submitting.")
    elif answer in wrong.answers:
        print(f"{answer} previously submitted and failed. Not submitting.")
    elif wrong.is_toohigh(answer):
        print(f"{answer} is too high; as {wrong.toohigh} was. Not submitting.")
    elif wrong.is_toolow(answer):
        print(f"{answer} is too low; as {wrong.toolow} was. Not submitting.")
    else:
        return True
    return False


should_wait = False
if not os.path.isfile(solution_file):
    should_wait = True
    write_to(solution_file, "from utils import *\n\n")


def do_part(part=None):
    global should_wait
    page, correct_answers = get_page(part)

    if not part:
        part = str(min(completed+1, 2 if day < 25 else 1))
    no_submit = False
    if int(part) <= completed:
        no_submit = True

    wrong = Wrong(part)
    old_wrong = Wrong("1")

    find_examples(part, page)

    ns = 0
    if should_wait:
        wait_for_changes(solution_file)
    while True:
        while ns == (ns := os.stat(solution_file).st_mtime_ns):
            wait_for_changes(solution_file)
        ns = os.stat(solution_file).st_mtime_ns

        should_wait = False

        print()

        good_answers, unknown_answers, all_passed = run_examples(part)
        example_answers = good_answers + unknown_answers

        if not all_passed:
            continue

        if not good_answers:
            print("No examples were verified, so the result will not be submitted without confirmation")

        answer, p1answer = run_real(part)
        if not answer:
            continue

        p1wrong = False
        if part == "2" and p1answer and p1answer != correct_answers[0]:
            print(f"Warning: Part 1 answer regressed (expecting {correct_answers[0]}, got {p1answer})")
            p1wrong = True

        print("Verified example answers: ", good_answers)
        print("Unverified example answers: ", unknown_answers)
        print("Real answer: ", answer)

        if no_submit:
            print("\nNot submitting, as already completed.")
            correct_answer = correct_answers[int(part)-1]
            if answer == correct_answer:
                print("Correct answer." + (" But, part 1 was wrong." if p1wrong else ""))
                exit(int(p1wrong))
            else:
                print(f"Incorrect answer. Expecting {correct_answer}")
                exit(1)

        if part == "2" and answer in old_wrong.answers:
            print(f"{answer} was previously incorrectly submitted for part 1. Did you accidentally solve part 2 first?")

        if not answer_checks(answer, example_answers, correct_answers, wrong, part):
            continue

        print("")
        should_prompt = wrong.answers or old_wrong.answers or p1wrong
        if (good_answers and not should_prompt) or input(f"Do you want to submit {repr(answer)} (y/n)?").lower() == "y":
            print("Submitting answer:", repr(answer))
            content, passed, failed = submit(part=part, answer=answer)
            if passed:
                should_wait = True
                if day == 25 and part == "1":
                    submit(part="2", answer="0")
                    exit(0)
                break
            elif failed:
                wrong.add_bad(answer, content)
            else:
                print("\nDid not recognise success or incorrect, may be timeout or blank input or already completed")

    return part


touch(real_inputfile)
touch(solution_file)

wait_for_unlock(day, year)

real_input = get_or_save(dayurl + "/input", real_inputfile).splitlines()
print("\nReal input stats:")
print_input_stats(real_input)
print()

if part_arg:
    do_part(part_arg)
else:
    if do_part() == "1":
        do_part("2")
