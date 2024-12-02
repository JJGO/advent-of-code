import math
import operator
from collections import Counter
from functools import reduce


def parses(input):
    data = []
    for line in input.strip().split("\n"):
        g, line = line.split(": ")
        game = []
        for set_ in line.split("; "):
            cubes = []
            for x in set_.split(", "):
                n, color = x.split(" ")
                n = int(n)
                cubes.append((color, n))
            game.append(cubes)
        data.append((int(g.split(" ")[1]), game))
    return data


def solve_a(data):
    total = 0
    valid = Counter({"red": 12, "green": 13, "blue": 14})
    for i, game in data:
        counts = [Counter(dict(set_)) for set_ in game]
        max_counts = reduce(operator.or_, counts)
        # Counters don't go negative
        if len(max_counts - valid) == 0:
            total += i
    return total


def solve_b(data):
    total = 0
    for i, game in data:
        counts = [Counter(dict(set_)) for set_ in game]
        # Counter1 | Counter2 takes max elementwise
        max_counts = reduce(operator.or_, counts)
        total += math.prod(max_counts.values())
    return total


sample = parses(
    """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=2)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 8
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 2286
    puzzle.answer_b = solve_b(data)
