from itertools import accumulate, cycle


def parses(input):
    return [int(x) for x in input.strip().split("\n")]


def partA(vals):
    return sum(vals)


def partB(vals):
    seen = set([0])
    cumsum = 0
    for cumsum in accumulate(cycle(vals)):
        if cumsum in seen:
            return cumsum
        seen.add(cumsum)


samplesA = [
    ([+1, +1, +1], 3),
    ([+1, +1, -2], 0),
    ([-1, -2, -3], -6),
]

samplesB = [
    ([+1, -1], 0),
    ([+3, +3, +4, -2, -4], 10),
    ([-6, +3, +8, +5, -6], 5),
    ([+7, +7, -2, -7, -4], 14),
]

if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2018, day=1)
    data = parses(puzzle.input_data)

    for s, sol in samplesA:
        assert partA(s) == sol
    puzzle.answer_a = partA(data)

    for s, sol in samplesB:
        assert partB(s) == sol
    puzzle.answer_b = partB(data)
