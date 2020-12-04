inp = open("input16").read()[:-1]
#inp = list('03036732577212944063491565474664')

offset = int(''.join(inp[:7]))
inp = [int(i) for i in list(inp)]


def pat(j, k):
    return [0, 1, 0, -1][(k % (j*4))//j]


def base_fft(inp, pat_off=1):
    out = []
    for i in range(len(inp)):
        j = i+1
        tot = sum([int(inp[k])*pat(j, k+pat_off) for k in range(len(inp))])
        out.append(abs(tot) % 10)


def part2(inp):
    out = []
    psum = 0
    for _, i in enumerate(inp):
        psum += i
        psum %= 10
        out.append(psum)
    return out


inp = (inp*10000)[offset:]
print('go')
print(len(inp), offset, offset*2)
'''
for i in range(100):
  inp = base_fft(inp)
  #print(i)
  print(i, ':', ''.join([str(i) for i in inp]))

print(''.join([str(i) for i in inp[:8]]))
print(''.join([str(i) for i in inp[offset:offset+8]]))
'''

inp = inp[::-1]
for i in range(100):
    inp = part2(inp)
inp = inp[::-1]
print(''.join([str(i) for i in inp[:8]]))
