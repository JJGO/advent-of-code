import re
def parses(data):
    return data


def solve_a(data):
    return sum(
        int(a)*int(b) for a, b in re.findall('mul\((\d+),(\d+)\)', data)
    )


def solve_b(data):
    do = True
    acc = 0
    pattern = "(mul\((\d+),(\d+)\)|do\(\)|don't\(\))"
    for action, a, b in re.findall(pattern, data):
        if action == "do()":
            do = True
        elif action == "don't()":
            do = False
        elif do and  "mul" in action:
            acc += int(a) * int(b)
    return acc


sample_a = parses("""xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))""")

sample_b = """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""

if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=3)
    data = parses(puzzle.input_data)
    assert solve_a(sample_a) == 168
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample_b) == 48
    puzzle.answer_b = solve_b(data)
