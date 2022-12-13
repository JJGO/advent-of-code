import numpy as np


def parses(input):
    data = list(map(list, input.strip().split("\n")))
    return np.array([[int(i) for i in row] for row in data])


def sizes(root):
    all_sizes = []

    def _helper(node):
        size = 0
        for file, content in node.items():
            if isinstance(content, int):
                size += content
            elif isinstance(content, dict):
                size += _helper(content)
        all_sizes.append(size)
        return size

    _helper(root)
    return all_sizes


def apply_all_directions(data, row_fn):
    return [
        np.rot90(np.apply_along_axis(row_fn, 1, np.rot90(data, i)), -i)
        for i in range(4)
    ]


def visible(row):
    cum_max = np.concatenate(([-1], np.maximum.accumulate(row)[:-1]))
    return row > cum_max


def scenic_score(row):
    score = np.zeros_like(row)
    for i, v in enumerate(row):
        for w in row[i + 1 :]:
            score[i] += 1
            if w >= v:
                break
    return score


def solve_a(data):
    return np.logical_or.reduce(apply_all_directions(data, visible)).sum()


def solve_b(data):
    return np.multiply.reduce(apply_all_directions(data, scenic_score)).max()


sample = parses(
    """30373
25512
65332
33549
35390"""
)

if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2022, day=8)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 21
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 8
    puzzle.answer_b = solve_b(data)
