import parse
from collections import deque, defaultdict


def parses(input):
    return parse.parse(
        "{:d} players; last marble is worth {:d} points", input.strip()
    ).fixed


samples = [
    (parses("10 players; last marble is worth 1618 points"), 8317),
    (parses("13 players; last marble is worth 7999 points"), 146373),
    (parses("17 players; last marble is worth 1104 points"), 2764),
    (parses("21 players; last marble is worth 6111 points"), 54718),
    (parses("30 players; last marble is worth 5807 points"), 37305),
]


def play(nplayers, nmarbles, times=1):
    circle = deque([0])
    scores = defaultdict(int)
    for m in range(1, nmarbles * times + 1):
        if m % 23 == 0:
            circle.rotate(7)
            scores[m % nplayers] += circle.popleft() + m
        else:
            circle.rotate(-2)
            circle.appendleft(m)
    return max(scores.values())


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2018, day=9)
    data = parses(puzzle.input_data)
    for sample, sol in samples:
        assert play(*sample) == sol
    puzzle.answer_a = play(*data)
    puzzle.answer_b = play(*data, times=100)
