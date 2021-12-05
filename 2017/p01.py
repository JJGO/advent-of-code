def captcha(s):
    s += s[0]
    return sum(
        int(s[i]) for i in range(len(s) - 1) if s[i] == s[i+1]
    )


def captchaB(s):
    N = len(s)
    return sum(
        int(s[i]) for i in range(N) if s[i] == s[(i + N//2) % N]
    )


samplesA = [
    ("1122", 3),
    ("1111", 4),
    ("1234", 0),
    ("91212129", 9),
]

samplesB = [
    ("1212", 6),
    ("1221", 0),
    ("123425", 4),
    ("123123", 12),
    ("12131415", 4),
]


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2017, day=1)

    data = puzzle.input_data

    for s, sol in samplesA:
        assert captcha(s) == sol

    puzzle.answer_a = captcha(data)

    for s, sol in samplesB:
        assert captchaB(s) == sol

    puzzle.answer_b = captchaB(data)
