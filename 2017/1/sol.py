inp = open("2017/1.in").read().strip()
inp += inp[0]

s = 0
for d, nd in zip(inp, inp[1:]):
    if d == nd:
        s += int(d)

print(s)
