def parses(input):
    lines = []
    for line in input.split("\n"):
        pre, *post = map(int, line.replace(":", "").split())
        lines.append((pre, post))
    return lines


add = lambda x, y: x + y
mul = lambda x, y: x * y
concat = lambda x, y: int(str(x) + str(y))


def solve(data, ops):
    def is_feasible(total, nums):
        valid = set([nums[0]])
        for num in nums[1:]:
            valid = {op(x, num) for x in valid for op in ops}
            valid = {x for x in valid if x <= total}
        return total in valid

    return sum(total for total, nums in data if is_feasible(total, nums))


def solve_a(data):
    return solve(data, [add, mul])


def solve_b(data):
    return solve(data, [add, mul, concat])


def solve_fast(data, part_b=False):
    # Faster solution that works backwards from the total, pruning
    # concatenation and multiplication paths that are not feasible
    # If last operation is multiplication, then total must be divisible by last number
    # If last operation is concatenation, then last number must be a strict suffix of total
    def is_possible(total, nums):
        if len(nums) == 0:
            return False
        if len(nums) == 1:
            return total == nums[0]

        *prefix, last = nums

        last_s = str(last)
        total_s = str(total)
        # If last concatenation is not correct, prune path
        if (
            part_b
            and total_s[1:].endswith(last_s)
            and is_possible(int(total_s[: -len(last_s)]), prefix)
        ):
            return True

        # If last multiplication is not correct, prune path
        if total % last == 0 and is_possible(total // last, prefix):
            return True

        new_total = total - last
        if new_total > 0 and is_possible(new_total, prefix):
            return True

        return False

    return sum(total for total, nums in data if is_possible(total, nums))


def solve_a(data):
    return solve_fast(data, part_b=False)


def solve_b(data):
    return solve_fast(data, part_b=True)


sample = parses(
    """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=7)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 3749
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 11387
    puzzle.answer_b = solve_b(data)
