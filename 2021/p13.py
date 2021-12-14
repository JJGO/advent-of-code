import parse


def parses(input):
    coords = [tuple(x) for x in parse.findall("{:d},{:d}", input)]
    instructions = [tuple(x) for x in parse.findall("{:l}={:d}", input)]
    return coords, instructions


def fold(coords, instructions):
    coords = set(coords)
    for dim, fold in instructions:
        d = "xy".index(dim)
        for point in list(coords):
            if point[d] > fold:
                coords.remove(point)
                coords.add(
                    tuple(v if i != d else 2 * fold - v for i, v in enumerate(point))
                )
    return coords


def render(coords, chars=".#"):
    N = max(j for i, j in coords)
    M = max(i for i, j in coords)
    s = ""
    for j in range(N + 1):
        for i in range(M + 1):
            s += chars[(i, j) in coords]
        s += "\n"
    return s


def solve_a(data):
    coords, instructions = data
    return len(fold(coords, instructions[:1]))


def solve_b(data):
    print(render(fold(*data), chars=" █"))


def overkill_b(data):
    import numpy as np
    from PIL import Image
    import pytesseract

    coords = fold(*data)
    N = max(i for i, j in coords) + 1
    M = max(j for i, j in coords) + 1
    im = np.zeros((N, M))
    for x, y in coords:
        im[x, y] = 1
    im2 = Image.fromarray(255 * (1 - np.pad(im.T, 2))).convert("RGB")
    H, W = im2.size
    imL = im2.resize((H * 7, W * 7), Image.NEAREST)
    ocr = pytesseract.image_to_string(imL).strip()
    print(ocr)
    return ocr


sample = parses(
    """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2021, day=13)
    data = parses(puzzle.input_data)

    assert solve_a(sample) == 17
    puzzle.answer_a = solve_a(data)

    solve_b(sample)
    solve_b(data)
    puzzle.answer_b = overkill_b(data)
