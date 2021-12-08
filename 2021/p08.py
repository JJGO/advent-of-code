import itertools
from collections import Counter


def parses(input):
    return [
        tuple([s.split() for s in line.split(" | ")])
        for line in input.strip().split("\n")
    ]


def normalize(s):
    return "".join(sorted(s))


def list2num(nums):
    return int("".join([str(n) for n in nums]))


def solve_a(data):
    return sum(sum(1 for v in right if len(v) in [2, 4, 3, 7]) for _, right in data)


def fastsolve_b(data):
    # Deduction from the digits placement
    total = 0
    for left, right in data:

        left = [set(v) for v in left]
        nums = {}

        nums[1] = next(v for v in left if len(v) == 2)
        nums[7] = next(v for v in left if len(v) == 3)
        nums[4] = next(v for v in left if len(v) == 4)
        nums[8] = next(v for v in left if len(v) == 7)
        nums[6] = next(v for v in left if len(v) == 6 and (v | nums[7] == nums[8]))
        nums[9] = next(v for v in left if len(v) == 6 and nums[4].issubset(v))
        nums[5] = nums[6] & nums[9]
        nums[0] = next(v for v in left if len(v) == 6 and v != nums[6] and v != nums[9])
        nums[2] = next(v for v in left if len(v) == 5 and (v | nums[5]) == nums[8])
        nums[3] = next(v for v in left if len(v) == 5 and nums[7].issubset(v))

        reverse = {normalize(v): k for k, v in nums.items()}
        nright = [reverse[normalize(v)] for v in right]
        total += list2num(nright)

    return total


# Alternative solutions for B
num2segments = {
    0: "abcefg",
    1: "cf",
    2: "acdeg",
    3: "acdfg",
    4: "bcdf",
    5: "abdfg",
    6: "abdefg",
    7: "acf",
    8: "abcdefg",
    9: "abcdfg",
}
segments2num = {v: k for k, v in num2segments.items()}


def bycounts_b(data):
    total = 0
    # How many times is each segment used, e.g a->8
    segment_counts = Counter("".join(segments2num.keys()))
    # Represent each digit by a hash from the sum of its segment_counts, which is unique
    digits = {
        sum(segment_counts[c] for c in segments): num
        for segments, num in segments2num.items()
    }
    for left, right in data:
        left = list(map(normalize, left))
        right = list(map(normalize, right))
        segment_counts = Counter("".join(left))
        mapping = {
            segments: digits[sum(segment_counts[c] for c in segments)]
            for segments in left
        }
        total += list2num([mapping[segments] for segments in right])
    return total


def bruteforce_b(data):
    total = 0
    for left, right in data:
        for perm in itertools.permutations("abcdefg"):
            remap = {new: orig for orig, new in zip("abcdefg", perm)}
            translated_left = [normalize(remap[c] for c in s) for s in left]
            if all(s in segments2num for s in translated_left):
                translated_right = [normalize(remap[c] for c in s) for s in right]
                total += list2num([segments2num[v] for v in translated_right])
                break
    return total


sample1 = parses(
    "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"
)
sample2 = parses(
    """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2021, day=8)
    data = parses(puzzle.input_data)

    assert solve_a(sample2) == 26
    puzzle.answer_a = solve_a(data)

    for solve_b in [
        fastsolve_b,
        bycounts_b,
        bruteforce_b,
    ]:

        assert solve_b(sample1) == 5353
        assert solve_b(sample2) == 61229
        puzzle.answer_b = solve_b(data)
