from typing import List, Tuple
import itertools


def parses(input):
    return input.strip().split("\n")


# Verbose solution but that nicely packs all the logic
# required to solve the problem in a couple of ways
# We are dealing with Balanced Base-5 system.
# We can either operate in this system or convert to
# decimal and back
class IntB5:

    VALUES = dict(zip("=-012", (-2, -1, 0, 1, 2)))
    CHARS = dict(zip((-2, -1, 0, 1, 2), "=-012"))

    def __init__(self, digits):
        self.digits: Tuple[int, ...] = tuple(digits)

    @classmethod
    def decode(cls, s: str) -> "IntB5":
        return IntB5([cls.VALUES[c] for c in s])

    def encode(self) -> str:
        return "".join(self.CHARS[d] for d in self.digits)

    def __add__(self, other: "IntB5") -> "IntB5":
        sum_digits = []
        carry = 0
        for a, b in itertools.zip_longest(
            reversed(self.digits), reversed(other.digits), fillvalue=0
        ):
            s, carry = a + b + carry, 0
            if s > 2:
                s -= 5
                carry += 1
            elif s < -2:
                s += 5
                carry -= 1
            sum_digits.append(s)
        if carry != 0:
            sum_digits.append(carry)
        return IntB5(reversed(sum_digits))

    def __repr__(self):
        return f"{self.__class__.__name__}({self.digits})"

    def __int__(self):
        acc = 0
        for d in self.digits:
            acc = 5 * acc + d
        return acc

    @classmethod
    def fromint(cls, x):
        digits = []
        while x > 0:
            # This logic is equivalent to:
            # x,r=divmod(x,5) ; if r>2: r-=5; x+=1
            x, r = divmod(x + 2, 5)
            digits.append(r - 2)
        return IntB5(reversed(digits))


sample = parses(
    """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"""
)


def solve_a_native(data):
    return sum(((IntB5.decode(x)) for x in data), start=IntB5((0,))).encode()


def solve_a_int(data):
    nums = [int(IntB5.decode(x)) for x in data]
    return IntB5.fromint(sum(nums)).encode()


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2022, day=25)
    data = parses(puzzle.input_data)
    for solve_a in solve_a_native, solve_a_int:
        assert solve_a(sample) == "2=-1=0"
        puzzle.answer_a = solve_a(data)
