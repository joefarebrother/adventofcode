from utils import *

new = 0
old = 0


class Monkey:
    def __init__(self, gr):
        id, items, op, test, true, false = gr
        self.id = ints_in(id)[0]
        self.items = ints_in(items)
        self.op = op[len("  Operation: new ="):].strip()
        self.test = ints_in(test)[0]
        self.true = ints_in(true)[0]
        self.false = ints_in(false)[0]
        self.activity = 0

    def turn(self):
        global old
        if not self.items:
            return

        for item in self.items:
            old = item
            item = eval(self.op)
            # print(self.id, old, item, item//3, (item//3) % self.test, self.true, self.false)
            # item //= 3
            item %= big_mod
            if not (item % self.test):
                monkeys[self.true].items.append(item)
            else:
                monkeys[self.false].items.append(item)
            self.activity += 1
        self.items = []


monkeys = [Monkey(gr) for gr in inp_groups()]
big_mod = math.prod((m.test for m in monkeys))

for i in range(10000):
    for m in monkeys:
        m.turn()
    print(i, [m.items for m in monkeys])

acts = sorted(m.activity for m in monkeys)
print(acts, acts[-2:], math.prod(acts[-2:]))
