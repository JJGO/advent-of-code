import numpy as np


def parses(input):
    draws, *boards = input.strip().split("\n\n")
    draws = [int(i) for i in draws.split(",")]
    boards = [
        [[int(i) for i in line.split()] for line in board.split("\n")]
        for board in boards
    ]
    return np.array(draws, dtype=np.int32), np.array(boards, dtype=np.int32)


def bingo(draws, boards):
    called = np.zeros_like(boards)
    for n in draws:
        called |= boards == n
        win = called.all(1).any(1) | called.all(2).any(1)
        if win.any():
            b = win.argmax()
            return n * (boards[b] * (1 - called[b])).sum()


def bingoall(draws, boards):
    called = np.zeros_like(boards)
    for n in draws:
        called |= boards == n
        win = called.all(1).any(1) | called.all(2).any(1)
        if win.all():
            return n * (boards[b] * (1 - called[b])).sum()
        b = win.argmin()


sample = parses(
    """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2021, day=4)
    data = parses(puzzle.input_data)
    assert bingo(*sample) == 4512
    puzzle.answer_a = bingo(*data)
    assert bingoall(*sample) == 1924
    puzzle.answer_b = bingoall(*data)
