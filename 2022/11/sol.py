from utils import *

monkeys = []
big_mod = 0


class Monkey:
    def __init__(self, gr):
        id_, items, op, test, true, false = gr
        self.id = ints_in(id_)[0]
        self.items = ints_in(items)
        self.op = eval("lambda old: " + op.split("=")[1].strip())
        self.test = ints_in(test)[0]
        self.true = ints_in(true)[0]
        self.false = ints_in(false)[0]
        self.activity = 0

    def turn(self, part2):
        for item in self.items:
            item = self.op(item)
            # print(self.id, old, item, item//3, (item//3) % self.test, self.true, self.false)
            if part2:
                item %= big_mod
            else:
                item //= 3
            if item % self.test == 0:
                monkeys[self.true].items.append(item)
            else:
                monkeys[self.false].items.append(item)
            self.activity += 1
        self.items = []


def do(rounds, part2):
    global monkeys, big_mod
    monkeys = [Monkey(gr) for gr in inp_groups()]
    big_mod = math.prod(m.test for m in monkeys)

    for _ in range(rounds):
        for m in monkeys:
            m.turn(part2)
    acts = sorted(m.activity for m in monkeys)
    return math.prod(acts[-2:])


print("Part 1:", do(20, False))
print("Part 2:", do(10000, True))
