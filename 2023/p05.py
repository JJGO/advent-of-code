import re


def get_nums(line):
    return [int(i) for i in re.findall("\d+", line)]


def parses(input):
    seeds, *maps = input.strip().split("\n\n")
    seeds = get_nums(seeds)

    parsed_maps = []
    for map_ in maps:
        _, *lines = map_.split("\n")
        parsed_maps.append([get_nums(line) for line in lines])
    return seeds, parsed_maps


def solve_a(data):
    vals, maps = data
    maps = [sorted([(src, length, dst) for dst, src, length in map_]) for map_ in maps]

    for map_ in maps:
        new_vals = []
        for val in vals:
            for src, length, dst in map_:
                if src <= val < src + length:
                    new_vals.append(val - src + dst)
                    break
            else:
                new_vals.append(val)
        vals = new_vals
    return min(vals)


def solve_b(data):
    vals, maps = data
    vals = [(i, i + n) for i, n in zip(vals[::2], vals[1::2])]
    maps = [sorted([(src, src + m, dst) for dst, src, m in map_]) for map_ in maps]

    for map_ in maps:
        new_vals = []
        for s1, e1 in vals:
            for s2, e2, dst in map_:
                if e1 < s2:
                    break
                if s2 <= s1 and e1 <= e2:
                    # completely inside
                    new_vals.append((dst + s1 - s2, dst + e1 - s2))
                    s1 = e1
                    break
                if s2 <= s1 < e2:
                    # partially inside
                    new_vals.append((dst + s1 - s2, dst + e2 - s2))
                    s1 = e2
                    continue
                if s1 <= s2 < e1:
                    # partially outside
                    new_vals.append((s1, s2))
                    s1 = s2
                    continue
            if e1 - s1 > 0:
                new_vals.append((s1, e1))
        vals = new_vals
    return min(vals)[0]


sample = parses(
    """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=5)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 35
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 46
    puzzle.answer_b = solve_b(data)
