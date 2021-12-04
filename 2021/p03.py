import numpy as np


def parses(input):
    return np.array([[int(i) for i in line] for line in input.strip().split()])


def tobin(x):
    return (2 ** np.arange(len(x)) * x[::-1]).sum()


def partA(x):
    N = len(x)
    common = x.sum(0) >= N / 2
    return tobin(common) * tobin(1 - common)


def partB(x):
    def filtercommon(x, toggle=0):
        for i in range(x.shape[1]):
            if x.shape[0] == 1:
                break
            common = int(x[:, i].sum() >= x.shape[0] / 2)
            x = x[x[:, i] == common ^ toggle]
        return tobin(x[0])

    return filtercommon(x, 0) * filtercommon(x, 1)


sample = parses(
    """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""
)

if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2021, day=3)
    data = parses(puzzle.input_data)
    assert partA(sample) == 198
    puzzle.answer_a = partA(data)
    assert partB(sample) == 230
    puzzle.answer_b = partB(data)
