def parses(input):
    return [
        tuple([int(i) for i in line.split(",")]) for line in input.strip().split("\n")
    ]


def neighbors(x, y, z):
    return [
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y + 1, z),
        (x, y - 1, z),
        (x, y, z + 1),
        (x, y, z - 1),
    ]


def solve_a(data):
    total = 0
    seen = set()
    for point in data:
        total += sum(1 if n not in seen else -1 for n in neighbors(*point))
        seen.add(point)
    return total


def solve_b(data):
    # flood-fill the outside and count everytime that we see a rock
    # if we see the same rock multiple times that is fine since
    # we will do from different faces
    surface = 0
    mins = tuple([min(axis) - 1 for axis in zip(*data)])
    maxs = tuple([max(axis) + 1 for axis in zip(*data)])
    rock = set(data)
    stack = [mins]
    visited = set(stack)
    while stack:
        point = stack.pop()
        for neighbor in neighbors(*point):
            if all(min_ <= c <= max_ for c, min_, max_ in zip(neighbor, mins, maxs)):
                if neighbor in rock:
                    surface += 1
                elif neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)
    return surface


sample = parses(
    """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2022, day=18)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 64
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 58

    puzzle.answer_b = solve_b(data)
