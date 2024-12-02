def parses(text):
    return [[int(i) for i in line.split()] for line in text.split("\n")]


def checksum(sheet):
    return sum([max(line) - min(line) for line in sheet])


def divisible(sheet):
    def _divisible(line):
        line = sorted(line)
        for i, n in enumerate(line):
            for m in line[i + 1 :]:
                d, r = divmod(m, n)
                if r == 0:
                    return d

    return sum(_divisible(line) for line in sheet)


sampleA = parses(
    """5 1 9 5
7 5 3
2 4 6 8"""
)

sampleB = parses(
    """5 9 2 8
9 4 7 3
3 8 6 5"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2017, day=2)

    data = parses(puzzle.input_data)

    assert checksum(sampleA) == 18
    puzzle.answer_a = checksum(data)

    assert divisible(sampleB) == 9
    puzzle.answer_b = divisible(data)
