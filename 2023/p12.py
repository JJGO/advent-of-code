from functools import lru_cache


def parses(input):
    rows = []
    for line in input.strip().split("\n"):
        conditions, groups = line.split(" ")
        groups = tuple([int(n) for n in groups.split(",")])
        rows.append((conditions, groups))
    return rows


@lru_cache
def num_ways(conditions, groups):
    # if no groups, remainder must be all .
    if len(groups) == 0:
        return all(c in ".?" for c in conditions)
    # if groups, string must be long enough to at least fit them
    s = sum(groups) + len(groups) - 1
    if len(conditions) < s:
        return 0
    if sum(c in ("#?") for c in conditions) < sum(groups):
        return 0

    i = 0
    while (c := conditions[i]) == ".":
        i += 1
    g = groups[0]

    if_damaged = 0
    if c in "#?":
        N = len(conditions)
        if all(d in "#?" for d in conditions[i : i + g]) and (
            i + g == N or conditions[i + g] in "?."
        ):
            if_damaged = num_ways(conditions[i + g + 1 :], groups[1:])

    if c == "?":
        if_op = num_ways(conditions[i + 1 :], groups)
    else:
        if_op = 0

    return if_damaged + if_op


def solve_a(data):
    return sum([num_ways(*row) for row in data])


def solve_b(data):
    data = [("?".join(c for _ in range(5)), g * 5) for c, g in data]
    return solve_a(data)


sample = parses(
    """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=12)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 21
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 525152
    puzzle.answer_b = solve_b(data)
