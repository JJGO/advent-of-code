def parses(input):
    return [[int(i) for i in row] for row in input.strip().split("\n")]


from heapq import heappush, heappop


def best_path(data, least, most):
    visited = set()
    N, M = len(data), len(data[0])
    heap = [(0, 0, 0, 0, 1, 0), (0, 0, 0, 0, 1j, 0)]

    map_ = {i + 1j * j: data[i][j] for i in range(N) for j in range(M)}

    k = 0
    while heap:
        _, cost, _, pos, delta, momentum = heappop(heap)

        if pos == (N - 1) + 1j * (M - 1):
            return cost
        if (pos, delta, momentum) in visited:
            continue
        visited.add((pos, delta, momentum))

        if momentum < least:
            valid_deltas = [delta]
        elif momentum < most:
            valid_deltas = [delta, 1j * delta, -1j * delta]
        else:
            valid_deltas = [1j * delta, -1j * delta]

        for new_delta in valid_deltas:
            new_pos = pos + new_delta
            if new_pos not in map_:
                continue

            new_cost = cost + map_[new_pos]
            new_bound = new_cost + abs(N - 1 - new_pos.real) + abs(M - 1 - new_pos.imag)
            new_momentum = momentum + 1 if delta == new_delta else 1
            new_state = ( new_bound, new_cost, (k := k + 1), new_pos, new_delta, new_momentum,)

            if (new_pos, new_delta) not in visited:
                heappush(heap, new_state)


def solve_a(data):
    return best_path(data, 1, 3)


def solve_b(data):
    return best_path(data, 4, 10)


sample = parses(
    """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2023, day=17)
    data = parses(puzzle.input_data)
    assert solve_a(sample) == 102
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 94
    puzzle.answer_b = solve_b(data)
