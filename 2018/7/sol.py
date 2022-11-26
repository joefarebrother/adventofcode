import sys
import re
from collections import defaultdict

inp = list(open(sys.argv[1]))
ex = "test" in sys.argv[1]

prereq = defaultdict(set)
for line in inp:
    pre, post = re.findall(
        r'Step (.) must be finished before step (.) can begin.', line)[0]
    prereq[post].add(pre)
    prereq[pre]

print(prereq)

done = []
while len(done) < len(prereq):
    print(done)
    todo = [n for n, pre in prereq.items() if pre <= set(done)
            and n not in done]
    done.append(min(todo))

print("".join(done))


class Worker:
    def __init__(self) -> None:
        self.task = None
        self.time = -1

    def step(self):
        if self.task:
            self.time -= 1
            if not self.time:
                done.append(self.task)
                self.task = None

    def step2(self):
        if not self.task:
            n = next_task()
            if n:
                self.task = n
                started.append(n)
                self.time = time(n)


time_off = 0 if ex else 60
workers = [Worker() for i in range(2 if ex else 5)]


def time(a):
    return ord(a)-ord("A")+1+time_off


done = []
started = []


def next_task():
    todo = [n for n, pre in prereq.items() if pre <= set(done)
            and n not in started]
    if todo:
        return min(todo)


t = 0
while len(done) < len(prereq):
    print(t, end=" ")
    for w in workers:
        w.step()
        print(w.task, w.time, end=" ")
    for w in workers:
        w.step2()
    print("".join(done))
    t += 1
print(t-1)
