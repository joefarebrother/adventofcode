#! /usr/bin/env python3

# Based on https://github.com/penteract/adventofcode/blob/master/autotest.py

import urllib.request as r
from datetime import date, datetime
import os
import sys
import re
import platform
import math
from utils import get_day_year, wait_for_unlock, print_input_stats, numeric
from time import sleep

usage = """
Python script for advent of code which downloads the problem description,
attempts to extract sample input and corresponding output,
then runs sol.py on the sample input whenever sol.py is modified until
sol.py gives the sample output. When it does, sol gets run on the real input
and if that succeeds, the last printed word gets submitted automatically.

Call as `autotest.py {year} {day} [{part}]`, `autotest.py {day}`, or `autotest.py`; with the
environment variable $AOC_KEY set to the value of your session cookie.

If part is given, only run for the given part.

If called with the current day as input (which is the default if year and day are omitted), before the puzzle
unlocks at 5am GMT, waits until it unlocks. This assumes that the local timezone is GMT.

Files used, all under {year}/{day}:
sol.py      This program assumes that your solution for the part you are
            currently working on is in this file.
            Run as `python3 sol.py {input}` where {input} is the name of
            a file from which sol.py is expected to read the input
            for the day's problem

real.in      Your personal input (https://adventofcode.com/{year}/day/{day}/input)

test{n}.in  The automatically extracted sample input
            By default this is the first non-inline code block.
            It may be wrong, and if so you must manually edit it and restart this
            program if you want it to work correctly.
            If no appropriate sample input is found, the program will still run but will require confirmation before submitting results.
            Input 1 is generated automatically; subsequent inputs may be generated if they come from inline examples.
            Test input files can also be created manually and will be run. An empty example file or one that contains [NONE] will not be run.

test{n}-part{p}.out   The automatically extracted sample output for the given part
                      By default, this is the last highlighted thing at the end of a code tag.
                      It may be wrong, and if so you must manually edit it and restart this
                      program if you want it to work correctly.
                      If no appropriate sample output is found, this file will contain [NONE], 
                      and the program will still run but will require confirmation before submitting results.
                      An output file that doesn't exist or is empty will cause that example to be skipped; whereas one that contains [NONE] 
                      will cause the example to be run but its result won't be verified.

page{p}.html    the page when solving part {p}
pagefinal.html  the page after both parts have been solved.
wrong_ans       a text file containing a list of answers which have been rejected, as well as whether they were too high or low.
                Hopefully avoids repeatedly submitting wrong answers
                Does not distinguish between part 1 and part 2

timeout     Overrides the default example timeout of 10 seconds

tmp         stores the output of the solution on sample input
            Can be deleted without consequence except while the solution is running

tmpreal     stores the output of the solution on the real input
            Can be deleted without consequence except while the solution is running
"""

if __name__ != "__main__":
    raise Exception("Don't import autotest")

for arg in sys.argv[1:]:
    if "help" in arg or "-h" in arg:
        print(usage)
        exit(0)

sesh = os.environ["AOC_KEY"]
if not sesh:
    raise Exception("Environment variable AOC_KEY not set")

headers = {"Cookie": "session="+sesh}


def write_to(file, content):
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
            write_to(file, s)
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
workdir = os.path.normpath(f"{curdir}/{year}/{day}")+"/"
os.makedirs(workdir, exist_ok=True)

dayurl = f"https://adventofcode.com/{year}/day/{day}"

real_inputfile = f"{workdir}/real.in"
solution_file = f"{workdir}/sol.py"

wrong_ans_file = workdir + "wrong_ans"
bad_answers = set()
bad_toohigh = None
bad_toolow = None
if os.path.isfile(wrong_ans_file):
    with open(wrong_ans_file) as f:
        for line in f:
            if "[TOO HIGH]" in line:
                line = line.split()[0]
                bad_toohigh = min(int(line), bad_toohigh or math.inf)
            if "[TOO LOW]" in line:
                line = line.split()[0]
                bad_toolow = max(int(line), bad_toolow or -math.inf)
            bad_answers.add(line.strip())


def add_bad(ans, content):
    global bad_toohigh, bad_toolow
    extra = ""
    if "too high" in content:
        bad_toohigh = min(int(ans), bad_toohigh or math.inf)
        extra = " [TOO HIGH]"
    if "too low" in content:
        bad_toolow = max(int(ans), bad_toolow or -math.inf)
        extra = " [TOO LOW]"
    bad_answers.add(ans)
    with open(wrong_ans_file, mode="a") as f:
        print(ans + extra, file=f)


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


def find_examples(part, orig_s):
    if year == 2019 and "intcode" in read_string(solution_file):
        return

    test1_inputfile = f"{workdir}/test1.in"
    test1_outputfile = f"{workdir}/test1-part{part}.out"

    might_have_inline_ex = len(real_input) <= 2
    looked = False
    s = orig_s

    if not os.path.isfile(test1_inputfile):
        print("Trying to find sample input to save in ", test1_inputfile)
        looked = True

        eg = tags("code", tags("pre", s), True, True, False)
        if not eg:
            print("Could not find example (No <pre><code> tags)")
            write_to(test1_inputfile, "[NONE]")
        else:
            eg = eg[0]
            eg = eg.replace("<em>", "").replace("</em>", "")
            eg = html_entities(eg)
            write_to(test1_inputfile, eg)
            print("Assumed input:")
            print(eg)
    else:
        print("Assumed input:")
        print(read_string(test1_inputfile))

    if not os.path.isfile(test1_outputfile):
        print("Trying to find sample output to save in", test1_outputfile)
        looked = True

        find_res = s.find("--- Part Two ---")
        if find_res > -1:
            if part == "1":
                s = s[:find_res]
            else:
                s = s[find_res:]

        # lists may contain other examples, but (usually) not the answer to the current example
        if might_have_inline_ex:
            s = remove_tags("li", s)
        s = remove_tags("pre", s)

        o = tags("em", tags("code", s), exact_end=True) + \
            tags("code", tags("em", s), exact_end=True)
        if not o:
            print("Could not find example output (no <code><em> tag)")
            sample_out = "[NONE]"
            write_to(test1_outputfile, "[NONE]")
        else:
            sample_out = o[-1]
            write_to(test1_outputfile, sample_out)
    else:
        sample_out = read_string(test1_outputfile).strip()
        if sample_out == "[NONE]":
            print("No output specified.")
    print("Assumed output:", sample_out)

    if might_have_inline_ex and looked:
        s = orig_s
        # find more inline examples
        find_res = s.find("--- Part Two ---")
        if find_res > -1:
            if part == "1":
                s = s[:find_res]
            else:
                s = s[find_res:]

        s = remove_tags("pre", s)

        uls = tags("ul", s)
        if uls:
            ul = uls[-1]
            o = tags("em", tags("code", s), exact_end=True) + \
                tags("code", tags("em", s), exact_end=True)
            if o and (o[-1]+"</em></code>" in ul or o[-1]+"</code></em>" in ul):
                # last highlighted answer was in a ul tag; probably in inline example
                # 2018 day 8 part 2 is a counterexample
                lis = tags("li", ul)
                for li in lis:
                    codes = tags("code", li)
                    if len(codes) >= 2:
                        em = tags("em", codes, exact_end=True) + \
                            tags("code", tags("em", li), exact_end=True)
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
        if m:
            try:
                idx = int(m.groups(1)[0])
            except:
                continue
            inputfile = workdir+f
            outputfile = f"{workdir}/test{idx}-part{part}.out"
            if os.path.isfile(outputfile):
                if read_string(inputfile).strip() in ["[NONE]", ""]:
                    print(f"Example {idx} skipped: No input found")
                    continue
                if read_string(outputfile).strip() == "":
                    print(f"Example {idx} skipped: Output file empty")
                ans, suc = run_example(
                    inputfile, outputfile, idx, part, timeout)
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


def run_example(inputfile, outputfile, idx, part, timeout):
    """
    Runs a single example.
    Returns (ans, succ) where ans is the answer given, and succ is True if the test passed, False if it didn't, and None if no expected output was found.
    """
    tmpfile = workdir+"tmp"

    print(f"==== Trying example {idx} ({timeout} second timeout)\n")
    p = tee(
        f"timeout --foreground {timeout} python3 -u {solution_file} {inputfile}", tmpfile)
    if p:
        print(f"=== Example {idx} did not terminate successfully")
        return None, False

    ans = answer_in_out(read_string(tmpfile), part)

    if ans == None:
        print(f"=== Example {idx} produced no output")
        return None, False

    sample_out = read_string(outputfile).strip()
    if sample_out == "[NONE]":
        return ans, None

    if ans != sample_out:
        print(
            f"=== Example {idx} failed: Expected {sample_out}, got {ans}")
        return ans, False

    return ans, True


def run_real(part):
    tmpfile = workdir+"tmpreal"

    print("==== trying real input (no timeout)")
    p = tee(
        f"python3 -u {solution_file} {real_inputfile}", tmpfile)
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
                o = o[len("part 1"):].strip(":").split()
                if o:
                    return o[-1].strip("()[]{}")
            if o.lower().startswith("part 2") and part == "1":
                return None
        nout.append(o)
    nout = " ".join(nout).split()
    if nout:
        return nout[-1].strip("()[]{}")
    return None


submit_time = None
bad_submit_time = None


def submit(part, answer):
    global submit_time, bad_submit_time
    url = f"https://adventofcode.com/{year}/day/{day}/answer"
    print(f"Submitting", repr(answer), "to url", repr(url))
    if bad_submit_time != None:
        timeout = (datetime.now() - bad_submit_time).total_seconds()
        if timeout < 60:
            print(f"Waiting {timeout} seconds")
            sleep(61-timeout)
            print("Done")

    resp = r.urlopen(r.Request(url, data=bytes(
        f"level={part}&answer={answer}", "utf8"), headers=headers))

    submit_time = datetime.now()
    print("time", submit_time)
    print("response:")
    resp = "".join(l.decode() for l in resp)
    content = tags("article", resp)[0]
    print(content)
    return resp, content


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
    final_file = workdir+"pagefinal.html"
    if os.path.isfile(final_file):
        s = read_string(final_file)
    else:
        part_file = f"{workdir}/page{part}.html" if part else None
        s = get_or_save(dayurl, part_file)
    completed = s.count("Your puzzle answer was")
    if completed == 2:
        write_to(final_file, s)
    if completed == 1:
        write_to(workdir+"page2.html", s)
    if completed == 0:
        write_to(workdir+"page1.html", s)
        if part == "2":
            raise Exception("Con't do part 2 without having completed part 1")
    return s


def do_part(part=None):
    global bad_submit_time, should_wait
    s = get_page(part)
    completed = s.count("Your puzzle answer was")
    if not part:
        part = str(min(completed+1, 2 if day < 25 else 1))
        print("\nReal input stats:")
        print_input_stats(real_input)
    no_submit = False
    if int(part) <= completed:
        no_submit = True
        correct_answers = []
        for p in tags("p", s):
            if p.startswith("Your puzzle answer was"):
                correct_answers.append(tags("code", p)[0])

    find_examples(part, s)

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

        if all_passed:
            if not good_answers:
                print(
                    "No examples were verified, so the result will not be submitted without confirmation")

            answer, p1answer = run_real(part)
            if not answer:
                continue
            p1wrong = False
            if part == "2" and p1answer and p1answer != correct_answers[0]:
                print(
                    f"Warning: Part 1 answer regressed (expecting {correct_answers[0]}, got {p1answer})")
                p1wrong = True

            print("Verified example answers: ", good_answers)
            print("Unverified example answers: ", unknown_answers)
            print("Real answer: ", answer)

            if no_submit:
                print("\nNot submitting, as already completed.")
                correct_answer = correct_answers[int(part)-1]
                if answer == correct_answer:
                    print("Correct answer." +
                          (" But, part 1 was wrong." if p1wrong else ""))
                    exit(int(p1wrong))
                else:
                    print(f"Incorrect answer. Expecting {correct_answer}")
                    exit(1)

            # do some checks on answer
            if len(answer) < 3:
                print(repr(answer), "looks too small. Not submitting")
            elif answer in good_answers + unknown_answers:
                print(repr(answer),
                      "is the same as the example output. Not submitting")
            elif not numeric(answer, len_limit=False) and numeric(example_answers[0], len_limit=False):
                print(
                    repr(answer), "isn't numeric, whereas the example output is. Not submitting.")
            elif answer in bad_answers:
                print(repr(answer), "previously submitted and failed. Not submitting.")
            elif bad_toohigh and int(answer) >= bad_toohigh:
                print(repr(answer),
                      f"is too high; as {bad_toohigh} was. Not submitting.")
            elif bad_toolow and int(answer) <= bad_toolow:
                print(repr(answer),
                      f"is too low; as {bad_toolow} was. Not submitting.")
            else:
                print("")
                if (good_answers and not bad_answers and not p1wrong) or input(f"Do you want to submit {repr(answer)} (y/n)?").lower() == "y":
                    print("Submitting answer:", repr(answer))
                    resp, content = submit(part=part, answer=answer)
                    if "That's the right answer!" in content:
                        bad_submit_time = None
                        should_wait = True
                        if day == 25 and part == "1":
                            submit(part="2", answer="0")
                            exit(0)
                        break
                    elif "That's not the right answer" in content:
                        add_bad(answer, content)
                        bad_submit_time = submit_time
                    else:
                        print(
                            "\nDid not recognise success or incorrect, may be timeout or blank input or already completed")

    return part


should_wait = not os.path.isfile(solution_file)

touch(real_inputfile)
touch(solution_file)

wait_for_unlock(day, year)

real_input = get_or_save(dayurl + "/input", real_inputfile).splitlines()
print()

if len(sys.argv) >= 4:
    do_part(sys.argv[3])
else:
    if do_part() == "1":
        do_part("2")
