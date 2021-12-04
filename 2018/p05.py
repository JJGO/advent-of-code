import string


def react(data):
    data = list(data)
    stack = []
    for c in data:
        # Either we use it to pop or we push it
        if stack and stack[-1] == c.swapcase():
            stack.pop()
        else:
            stack.append(c)
    return len(stack)


def detect(data):
    data = list(data)
    minlen = float("inf")
    for c in string.ascii_lowercase:
        d = [x for x in data if x.lower() != c]
        minlen = min(react(d), minlen)
    return minlen


sample = "dabAcCaCBAcCcaDA"


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2018, day=5)
    data = puzzle.input_data
    assert react(sample) == 10
    puzzle.answer_a = react(data)
    assert detect(sample) == 4
    puzzle.answer_b = detect(data)
