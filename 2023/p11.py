import itertools


def parses(input):
    return [[".#".index(val) for val in row] for row in input.strip().split("\n")]


def compute_distance(data, expansion_factor):
    N, M = len(data), len(data[0])
    points = []
    row_sums = [0 for _ in range(N)]
    col_sums = [0 for _ in range(M)]

    for i, row in enumerate(data):
        for j, val in enumerate(row):
            if val == 1:
                points.append((i, j))
                row_sums[i] += 1
                col_sums[j] += 1

    zero_cols = set([j for j, s in enumerate(col_sums) if s == 0])
    zero_rows = set([i for i, s in enumerate(row_sums) if s == 0])

    def mapping(zeros, N):
        mapping = {}
        current = 0
        for i in range(N):
            if i in zeros:
                current += expansion_factor
            else:
                mapping[i] = current
                current += 1
        return mapping

    row_mapping = mapping(zero_rows, N)
    col_mapping = mapping(zero_cols, N)
    expanded_points = [(row_mapping[i], col_mapping[j]) for i, j in points]

    total_dist = 0
    for (x, y), (x2, y2) in itertools.combinations(expanded_points, 2):
        total_dist += abs(x - x2) + abs(y - y2)

    return total_dist


sample = parses(
    """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=11)
    data = parses(puzzle.input_data)
    assert compute_distance(sample, 2) == 374
    puzzle.answer_a = compute_distance(data, 2)
    assert compute_distance(sample, 10) == 1030
    assert compute_distance(sample, 100) == 8410
    assert compute_distance(sample, 1000000) == 82000210
    puzzle.answer_b = compute_distance(data, 1000000)


