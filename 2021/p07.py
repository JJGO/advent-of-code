import math
import numpy as np


def parses(input):
    return [int(i) for i in input.split(",")]


def bruteA(nums):
    nums = np.array(nums)
    return min(abs(nums - i).sum() for i in range(nums.min(), nums.max() + 1))


def bruteB(nums):
    nums = np.array(nums)

    def cost(n):
        d = abs(nums - n)
        return (d * (d + 1) // 2).sum()

    return min(cost(i) for i in range(nums.min(), nums.max() + 1))


def partA(nums):
    # Median minimizes Mean Absolute Error
    nums = np.array(nums)
    med = round(np.median(nums))
    return abs(nums - med).sum()


def partB(nums):
    # Mean minimizes Mean Squared Error
    # We want to minimize e**2 + e
    nums = np.array(nums)

    def cost(n):
        d = abs(nums - n)
        return (d * (d + 1) // 2).sum()

    mean = nums.mean()
    return min(cost(math.floor(mean)), cost(math.ceil(mean)))


sample = parses("16,1,2,0,4,2,7,1,2,14")


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2021, day=7)
    data = parses(puzzle.input_data)

    for fnA, fnB in [(partA, partB), (bruteA, bruteB)]:
        assert fnA(sample) == 37
        puzzle.answer_a = fnA(data)

        assert fnB(sample) == 168
        puzzle.answer_b = fnB(data)
