from scipy.signal import correlate2d
import numpy as np


def parses(text):
    mapping, image = text.strip().split("\n\n")
    mapping = np.array([{".": 0, "#": 1}[i] for i in mapping], dtype=np.uint8)
    image = np.array(
        [[{".": 0, "#": 1}[i] for i in line] for line in image.split("\n")],
        dtype=np.uint8,
    )
    return mapping, image


def enhance(mapping, image, steps):
    kernel = 2 ** np.arange(9)[::-1].reshape((3, 3))
    bg = 0
    for _ in range(steps):
        idx = correlate2d(image, kernel, boundary="fill", fillvalue=bg)
        image = mapping[idx]
        bg = mapping[[0, 511][bg]]
    return image


def solve_a(data):
    # if bg were to be 1 at end, result would be +inf
    return enhance(*data, 2).sum()


def solve_b(data):
    return enhance(*data, 50).sum()


sample = parses(
    """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2021, day=20)
    data = parses(puzzle.input_data)

    assert solve_a(sample) == 35
    puzzle.answer_a = solve_a(data)

    assert solve_b(sample) == 3351
    puzzle.answer_b = solve_b(data)
