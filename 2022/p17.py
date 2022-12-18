import numpy as np

sample = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"


def simulate(data, steps):
    # constants
    pieces = {  # relative coords wrt bottom-left corner
        "-": np.array([(i, 0) for i in range(4)]),
        "+": np.array([(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]),
        "L": np.array([(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]),
        "|": np.array([(0, i) for i in range(4)]),
        "o": np.array([(0, 0), (0, 1), (1, 0), (1, 1)]),
    }
    piece_order = "-+L|o"
    height = {"-": 1, "+": 3, "L": 3, "|": 4, "o": 2}

    # state
    chamber = np.zeros((7, 1), dtype=np.uint8)
    maxy = -1

    j = 0
    DOWN, LEFT, RIGHT = np.array([0, -1]), np.array([-1, 0]), np.array([+1, 0])
    #
    maxy_increments = []
    for i in range(steps):
        piece_type = piece_order[i % len(piece_order)]
        piece = pieces[piece_type]

        x, y = 2, 4 + maxy  # as per the rules

        # pad if needed
        maxh = chamber.shape[1]
        h = height[piece_type]
        if y + h >= maxh:
            pad = np.zeros((7, y - h + maxh + 1), np.uint8)
            chamber = np.hstack([chamber, pad])

        # absolute location
        loc = np.array([x, y]) + piece

        while True:
            jet = {"<": LEFT, ">": RIGHT}[data[j]]
            j = (j + 1) % len(data)  # increment mod length

            new_loc = loc + jet

            # if possible move sideways
            if (
                new_loc[:, 0].min() >= 0
                and new_loc[:, 0].max() < 7
                and (chamber[tuple(new_loc.T)] == 0).all()
            ):
                loc = new_loc

            new_loc = loc + DOWN

            # if possible move down
            if new_loc[:, 1].min() >= 0 and (chamber[tuple(new_loc.T)] == 0).all():
                loc = new_loc
            else:
                # cannot move down
                chamber[tuple(loc.T)] = 1
                prev_maxy = maxy
                maxy = max(maxy, loc[:, 1].max())
                maxy_increments.append(maxy - prev_maxy)
                break

    return np.array(maxy_increments)


def solve_a(data):
    return np.sum(simulate(data, steps=2022))


def solve_b(data):
    # Idea is to ignore the board state altogether and just focus on what
    # we know must repeat (as per the question): the max_y increments.
    # There will be a loop in the increments, we just need to find the period
    # Fourier analysis seems tempting but it's actually simpler to just
    # do boolean cross correlation and pick offsets with high similarity
    maxy_incs = simulate(data, steps=10_000)

    def similarity(x):
        return np.array([(x[:-i] == x[i:]).sum() for i in range(1, len(x))])

    # correlate signal with shifted version and pick indices of high agreement
    s = similarity(maxy_incs)
    high_similarity = np.argwhere(s > len(s) / 2).T[0]
    periods = np.diff(high_similarity)
    # Check period uniqueness
    assert len(set(periods.tolist())) == 1
    period = periods[0]
    # there's a prefix that does not repeat, afterwards it repeats
    # luckily (or likely because of puzzle building constraints),
    # the prefix is the same length
    assert (maxy_incs[period : 2 * period] == maxy_incs[2 * period : 3 * period]).all()
    inc_period = maxy_incs[period : 2 * period]
    # Compute maxy_increment sum via modular arithmetic
    step = 1_000_000_000_000
    initial_inc = np.sum(maxy_incs[:period])  # prefix is different
    q, r = divmod(step, period)
    return initial_inc + (q - 1) * inc_period.sum() + inc_period[:r].sum()


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2022, day=17)
    data = puzzle.input_data
    assert solve_a(sample) == 3068
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 1514285714288
    puzzle.answer_b = solve_b(data)
