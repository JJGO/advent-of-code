import re


# Decided to parse the board as intervals rather than coordinate sets
# We keep rocks separate per x, y coordinate so lookups are fast
def parses(input):
    board, instructions = input.split("\n\n")
    instructions = [
        int(i) if i not in "RL" else i for i in re.split("(R|L)", instructions)
    ]

    lines = board.split("\n")
    H, W = len(lines), max(map(len, lines))
    h_rocks = [set() for _ in range(H)]
    w_rocks = [set() for _ in range(W)]

    widths = [None for _ in range(H)]
    heights = [[H, 0] for _ in range(W)]
    for i, line in enumerate(lines):
        w, prefix = len(line), len(line.strip())
        widths[i] = (w - prefix, w)
        for j, v in enumerate(line):
            if j >= widths[i][0]:
                heights[j][0] = min(heights[j][0], i)
                if j < widths[i][1]:
                    heights[j][1] = max(heights[j][1], i + 1)
            if v == "#":
                h_rocks[i].add(j)
                w_rocks[j].add(i)
    return (widths, heights, h_rocks, w_rocks), instructions


# Wrap logic here is quite straightforward
def solve_a(data):
    board, instructions = data
    widths, heights, h_rocks, w_rocks = board
    i, j = 0, widths[0][0]

    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    facing = 0
    for ins in instructions:
        if isinstance(ins, str):
            facing = (facing + {"L": -1, "R": +1}[ins]) % 4
            continue

        for _ in range(ins):
            di, dj = dirs[facing]
            i2, j2 = i + di, j + dj
            if i != i2:
                if i2 >= heights[j][1]:
                    i2 = heights[j][0]
                if i2 < heights[j][0]:
                    i2 = heights[j][1] - 1
            if j != j2:
                if j2 >= widths[i][1]:
                    j2 = widths[i][0]
                if j2 < widths[i][0]:
                    j2 = widths[i][1] - 1
            if j2 in h_rocks[i2] or i2 in w_rocks[j2]:
                break
            i, j = i2, j2

    return 1000 * (i + 1) + 4 * (j + 1) + facing


# Ended up hardcoding the cube layout but in a way where
# it was as part of the data and not as part of the code
# so the code works for both the sample and the input
def solve_b(data, edge_pairs):
    board, instructions = data
    widths, heights, h_rocks, w_rocks = board
    i, j = 0, widths[0][0]

    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    facing = 0
    for ins in instructions:
        if isinstance(ins, str):
            facing = (facing + {"L": -1, "R": +1}[ins]) % 4
            continue

        for _ in range(ins):
            di, dj = dirs[facing]
            i2, j2 = i + di, j + dj
            new_facing = facing
            if (
                i2 >= heights[j][1]
                or i2 < heights[j][0]
                or j2 >= widths[i][1]
                or j2 < widths[i][0]
            ):
                for (fromi, fromj), (toi, toj), turn, req_facing in edge_pairs:
                    if i in fromi and j in fromj and facing == req_facing:
                        if turn % 4 in (1, 3):
                            i2, j2 = toi[fromj.index(j)], toj[fromi.index(i)]
                        else:
                            i2, j2 = toi[fromi.index(i)], toj[fromj.index(j)]
                        new_facing = (facing + turn) % 4
                        break
                else:
                    raise ValueError("Could not teleport")
            if j2 in h_rocks[i2] or i2 in w_rocks[j2]:
                break
            i, j = i2, j2
            facing = new_facing

    return 1000 * (i + 1) + 4 * (j + 1) + facing


sample = parses(
    """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""
)

# We pair up edges so we only need to encode 7 pairs
# instead of 14. We also specify what is the turn (mod 3)
# that the change produces and what is the required facing
# direction to enter the "portal". This last bit is critical
# for corners (which are a corner case, lol) as the will
# teleport to a different position depending on which
# direction we are facing
edge_pairs_sample = [
    [([0], range(8, 12)), ([4], range(3, -1, -1)), 2, 3],
    [(range(0, 4), [8]), ([4], range(4, 8)), -1, 2],
    [(range(0, 4), [11]), (range(15, 11, -1), [15]), 2, 0],
    [(range(4, 8), [0]), ([11], range(12, 16)), 1, 2],
    [(range(4, 8), [11]), ([8], range(15, 11, -1)), 1, 0],
    [([7], range(4)), ([11], range(11, 7, -1)), 2, 1],
    [([7], range(4, 8)), (range(15, 11, -1), [8]), -1, 1],
]
# fmt: off
# turn is relative, so we can negate it, i.e. -t%4
# but facing is absolute, so we need to find the complement direction (f+t-2) % 4
edge_pairs_sample += [(b,a,-t%4,(f+t-2)%4) for a,b,t,f in edge_pairs_sample]
# fmt: on

edge_pairs_data = [
    [([0], range(50, 100)), (range(150, 200), [0]), 1, 3],
    [([0], range(100, 150)), ([[199], range(0, 50)]), 0, 3],
    [(range(0, 50), [50]), (range(149, 99, -1), [0]), 2, 2],
    [(range(0, 50), [149]), (range(149, 99, -1), [99]), 2, 0],
    [(range(50, 100), [50]), ([100], range(0, 50)), -1, 2],
    [([49], range(100, 150)), (range(50, 100), [99],), 1, 1],
    [([149], range(50, 100)), (range(150, 200), [49]), 1, 1],
]
# fmt: off
edge_pairs_data += [(b,a,-t%4,(f+t-2)%4) for a,b,t,f in edge_pairs_data]
# fmt: on


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2022, day=22)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 6032
    puzzle.answer_a = solve_a(data)

    assert solve_b(sample, edge_pairs_sample) == 5031
    puzzle.answer_b = solve_b(data, edge_pairs_data)
