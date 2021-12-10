def parses(input):
    return input.strip().split("\n")


matching = {"(": ")", "[": "]", "{": "}", "<": ">"}


def solve_a(data):
    points = {")": 3, "]": 57, "}": 1197, ">": 25137}
    total = 0
    for line in data:
        stack = []
        for c in line:
            if c in matching:
                stack.append(c)
            elif not stack or matching[stack.pop()] != c:
                total += points[c]
                break
    return total


def solve_b(data):
    points = {")": 1, "]": 2, "}": 3, ">": 4}
    scores = []
    for line in data:
        stack = []
        for c in line:
            if c in matching:
                stack.append(c)
            elif not stack or matching[stack.pop()] != c:
                break
        else:
            total = 0
            while stack:
                total = 5 * total + points[matching[stack.pop()]]
            scores.append(total)
    return sorted(scores)[len(scores) // 2]


sample = parses(
    """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2021, day=10)
    data = parses(puzzle.input_data)

    assert solve_a(sample) == 26397
    puzzle.answer_a = solve_a(data)

    assert solve_b(sample) == 288957
    puzzle.answer_b = solve_b(data)
