def parses(input):
    return input.strip().split(",")


def hash_(string):
    string = string.replace("\n", "")
    x = 0
    for c in string:
        x = ((x + ord(c)) * 17) % 256
    return x


def solve_a(data):
    return sum([hash_(s) for s in data])


def solve_b(data):
    boxes = [[] for _ in range(256)]

    for instruction in data:
        op = "pop" if "-" in instruction else "set"
        label, focal = instruction.replace("=", "-").split("-")
        box = hash_(label)
        for j, (l, _) in enumerate(boxes[box]):
            if l == label:
                if op == "pop":
                    boxes[box].pop(j)
                if op == "set":
                    boxes[box][j] = (label, int(focal))
                break
        else:
            if op == "set":
                boxes[box].append((label, int(focal)))

    return sum(
        (i + 1) * (j + 1) * focal
        for i, box in enumerate(boxes)
        for j, (_, focal) in enumerate(box)
    )


sample = parses("""rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7""")


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=15)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 1320
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 145
    puzzle.answer_b = solve_b(data)
