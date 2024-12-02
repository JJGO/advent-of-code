import re


def parses(input):
    data = []
    for line in input.strip().split("\n"):
        card, nums = line.split(": ")
        winning, have = nums.split(" | ")
        winning = [int(i) for i in re.findall("\d+", winning)]
        have = [int(i) for i in re.findall("\d+", have)]
        data.append((winning, have))
    return data


def solve_a(data):
    total = 0
    for winning, have in data:
        intersection = set(winning) & set(have)
        if len(intersection) > 0:
            total += 2 ** (len(intersection) - 1)
    return total


def solve_b(data):
    cards = [1 for _ in data]
    for i, (winning, have) in enumerate(data):
        match = len(set(winning) & set(have))
        for j in range(i + 1, i + 1 + match):
            if j < len(cards):
                cards[j] += cards[i]
    return sum(cards)


sample = parses(
    """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=4)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 13
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 30
    puzzle.answer_b = solve_b(data)
