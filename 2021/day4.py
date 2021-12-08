from utils import *

inp = groups(4)

nums = ints(inp[0].split(","))

boards = []
for gr in inp[1:]:
    board = []
    for line in gr.splitlines():
        row = line.split()
        board.append([[int(x), False] for x in row])
    boards.append(board)


def call(num):
    global boards
    for b in boards:
        for row in b:
            for col in row:
                if col[0] == num:
                    col[1] = True


def is_bingo(board):
    for row in board:
        if all(c[1] for c in row):
            return True
    for colpos in range(len(board[0])):
        if all(row[colpos][1] for row in board):
            return True
    return False


def score(board):
    return sum(sum(c[0] for c in row if not c[1]) for row in board)


won = set()
for n in nums:
    call(n)

    for i, b in enumerate(boards):
        if is_bingo(b) and not i in won:
            won.add(i)
            if len(won) == 1:
                print("Part 1: ", score(b)*n)
            if len(won) == len(boards):
                print("Part 2: ", score(b)*n)
                exit()
