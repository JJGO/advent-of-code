from functools import cache

def parses(data):
    patterns, designs =  data.strip().split('\n\n')
    patterns = patterns.split(', ')
    designs = designs.split('\n')
    return patterns, designs


def solve(data):
    patterns, designs = data

    @cache
    def num_ways(design):
        if design == '':
            return 1

        return sum([num_ways(design[len(pattern):])
                    for pattern in patterns
                    if design.startswith(pattern)])

    return [num_ways(design) for design in designs]

def solve_a(data):
    return sum((x>0 for x in solve(data)))

def solve_b(data):
    return sum(solve(data))



sample = parses("""r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb""")


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=19)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 6
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 16
    puzzle.answer_b = solve_b(data)
