import itertools
import numpy as np


def parses(text):
    return [[".>v".index(c) for c in line] for line in text.strip().split("\n")]


def solve_a(state):
    state = np.array(state)
    EMPTY, RIGHT, DOWN = 0, 1, 2

    for i in itertools.count(1):
        moves_right = (state == RIGHT) & (np.roll(state, -1, 1) == EMPTY)
        state = (state * (1 - moves_right)) + np.roll(moves_right, 1, 1) * RIGHT

        moves_down = (state == DOWN) & (np.roll(state, -1, 0) == EMPTY)
        state = (state * (1 - moves_down)) + np.roll(moves_down, 1, 0) * DOWN

        if moves_right.sum() + moves_down.sum() == 0:
            return i


sample = parses(
    """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""
)

if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2021, day=25)
    data = parses(puzzle.input_data)

    assert solve_a(sample) == 58
    puzzle.answer_a = solve_a(data)
