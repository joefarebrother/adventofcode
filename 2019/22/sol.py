from utils import *
inp = inp_readlines()


def do(N, rep):
    # (i * a + b)%N = pos of card i
    cards = (1, 0)

    def rev(cards):
        # x -> N-1 - x = -1 - x = -(x+1)
        return ((-cards[0]) % N, (-cards[1]-1) % N)

    def cut(cards, n):
        return (cards[0], (cards[1]-n) % N)

    def deal(cards, n):
        return ((cards[0]*n) % N, (cards[1]*n) % N)

    for line in inp:
        if line.startswith("deal i"):
            cards = rev(cards)
        elif line.startswith("cut"):
            cards = cut(cards, int(line[3:].strip()))
        elif line.startswith("deal w"):
            cards = deal(cards, int(line[len("deal with increment"):].strip()))
        else:
            print("Unknown: " + line)

    # repeat a bunch

    # rep = 101741582076661

    # i -> i*a + b
    # rep n times
    #i*a^2 + ab + b
    # i*a^3 + a^2b + ab + b
    # i*a^n + b*(sum j=0..n-1 a^j)
    #i*a^n + b*(a^n-1)/(a-1)

    a, b = cards
    an = pow(a, rep, N)

    A, B = an, b*(an-1) * mod_inv(a-1, N)

    # Position of card 2019
    p1 = (2019 * A + B) % N

    # Card in position 2020
    p2 = (2020 - B)*mod_inv(A, N) % N

    return p1, p2


print("Part 1:", do(10007, 1)[0])
print("Part 2:", do(119315717514047, 101741582076661)[1])
