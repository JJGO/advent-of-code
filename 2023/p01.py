import re

def parses(input):
    return input.strip().split('\n')

def solve_a(data):
    lines = [re.findall('\d', line) for line in data]
    return sum((int(l[0]+l[-1]) for l in lines))

def solve_b(data):
    def normalize(line):
        nums = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
        for i, n in enumerate(nums):
            line = line.replace(n, f'{n}{i:d}{n}')
        return line
    lines = [re.findall('\d', normalize(line)) for line in data]
    return sum((int(l[0]+l[-1]) for l in lines))

sample_a = parses("""1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet""")

sample_b = parses("""two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen""")


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=1)
    data = parses(puzzle.input_data)
    assert solve_a(sample_a) == 142
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample_b) == 281
    puzzle.answer_b = solve_b(data)
