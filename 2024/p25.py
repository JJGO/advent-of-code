import itertools


def parses(data):
    blocks = data.strip().split("\n\n")
    keys, locks = [], []
    for block in blocks:
        coords = set(
            [
                (i, j)
                for i, row in enumerate(block.split("\n"))
                for j, v in enumerate(row)
                if v == "#"
            ]
        )
        if (0, 0) in coords:
            locks.append(coords)
        else:
            keys.append(coords)
    return locks, keys


def solve_a(data):
    locks, keys = data
    return sum([len(key & lock) == 0 for key, lock in itertools.product(locks, keys)])


sample = parses(
    """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=25)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 3
    puzzle.answer_a = solve_a(data)
