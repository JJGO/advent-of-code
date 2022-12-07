from typing import List


def parses(text):
    return [[int(i) for i in grp.split("\n")] for grp in text.strip().split("\n\n")]


def max_calories(calories: List[List[int]]):
    return max(*map(sum, calories))

def top3_calories(calories: List[List[int]]):
    return sum(sorted(map(sum, calories))[-3:])

sample = parses(
    """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2022, day=1)
    data = parses(puzzle.input_data)
    assert max_calories(sample) == 24000
    puzzle.answer_a = max_calories(data)
    assert top3_calories(sample) == 45000
    puzzle.answer_b = top3_calories(data)
