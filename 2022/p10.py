import numpy as np


def parses(input):
    return [line.split() for line in input.strip().split("\n")]


sample = parses(
    "addx 15\naddx -11\naddx 6\naddx -3\naddx 5\naddx -1\naddx -8\naddx 13\naddx 4\nnoop\naddx -1\naddx 5\naddx -1\naddx 5\naddx -1\naddx 5\naddx -1\naddx 5\naddx -1\naddx -35\naddx 1\naddx 24\naddx -19\naddx 1\naddx 16\naddx -11\nnoop\nnoop\naddx 21\naddx -15\nnoop\nnoop\naddx -3\naddx 9\naddx 1\naddx -3\naddx 8\naddx 1\naddx 5\nnoop\nnoop\nnoop\nnoop\nnoop\naddx -36\nnoop\naddx 1\naddx 7\nnoop\nnoop\nnoop\naddx 2\naddx 6\nnoop\nnoop\nnoop\nnoop\nnoop\naddx 1\nnoop\nnoop\naddx 7\naddx 1\nnoop\naddx -13\naddx 13\naddx 7\nnoop\naddx 1\naddx -33\nnoop\nnoop\nnoop\naddx 2\nnoop\nnoop\nnoop\naddx 8\nnoop\naddx -1\naddx 2\naddx 1\nnoop\naddx 17\naddx -9\naddx 1\naddx 1\naddx -3\naddx 11\nnoop\nnoop\naddx 1\nnoop\naddx 1\nnoop\nnoop\naddx -13\naddx -19\naddx 1\naddx 3\naddx 26\naddx -30\naddx 12\naddx -1\naddx 3\naddx 1\nnoop\nnoop\nnoop\naddx -9\naddx 18\naddx 1\naddx 2\nnoop\nnoop\naddx 9\nnoop\nnoop\nnoop\naddx -1\naddx 2\naddx -37\naddx 1\naddx 3\nnoop\naddx 15\naddx -21\naddx 22\naddx -6\naddx 1\nnoop\naddx 2\naddx 1\nnoop\naddx -10\nnoop\nnoop\naddx 20\naddx 1\naddx 2\naddx 2\naddx -6\naddx -11\nnoop\nnoop\nnoop\n"
)


def solve_a(data):
    X, cycle, strength_sum = 1, 1, 0
    for ins, *args in data:
        for _ in range({"noop": 1, "addx": 2}[ins]):
            strength_sum += (cycle % 40 == 20) * X * cycle
            cycle += 1
        if ins == "addx":
            X += int(args[0])
    return strength_sum


def solve_b(data):
    X, cycle = 0, 0
    crt = np.zeros((6, 40), dtype=np.uint8)
    for ins, *args in data:
        for _ in range({"noop": 1, "addx": 2}[ins]):
            row = cycle // 40
            if cycle % 40 in (X, X + 1, X + 2):
                crt[row][cycle % 40] = 1
            cycle += 1
        if ins == "addx":
            X += int(args[0])
    render = np.where(crt, "█", " ")
    print("\n".join("".join(row) for row in render))
    print()
    # import PIL.Image
    # import pytesseract
    # crtp = np.pad(crt, 3)
    # crti = PIL.Image.fromarray(255*crtp)
    # crtr = crti.resize((400,100)) #, PIL.Image.NEAREST)
    # ocr = pytesseract.image_to_string(crtr).strip()
    # print(ocr)
    # return crtr


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2022, day=10)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 13140
    puzzle.answer_a = solve_a(data)
    solve_b(sample)
    solve_b(data)
