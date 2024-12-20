from heapq import heappush, heappop


def parses(data):
    walls = []
    for line in data.strip().split("\n"):
        x, y = line.split(",")
        walls.append((int(x), int(y)))
    return walls


def shortest_path(data, N=70):
    walls = set(data)

    def heuristic(x, y):
        return abs(x - N) + abs(y - N)

    heap = [(heuristic(0, 0), 0, 0, 0)]
    visited = set()

    while heap:
        _, cost, x, y = heappop(heap)
        if (x, y) == (N, N):
            return cost
        if (x, y) in visited:
            continue
        visited.add((x, y))
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            x2, y2 = x + dx, y + dy
            if (
                0 <= x2 <= N
                and 0 <= y2 <= N
                and (x2, y2) not in walls
                and (x2, y2) not in visited
            ):
                heappush(heap, (cost + 1 + heuristic(x2, y2), cost + 1, x2, y2))


def solve_a(data, N=70, steps=1024):
    return shortest_path(data[:steps], N=N)

def solve_b(data, N=70):
    a, b = 0, len(data)
    # binary search
    while b-a > 1:
        m = (a+b)//2

        s = shortest_path(data[:m], N=N)
        if s is None: # not feasible
            b = m
        else:
            a = m
    x, y = data[b-1] # [:b] has points 0...b-1
    return f'{x},{y}'



sample = parses("""5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0""")


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2024, day=18)
    data = parses(puzzle.input_data)
    assert solve_a(sample, N=6, steps=12) == 22
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample, N=6) == '6,1'
    puzzle.answer_b = solve_b(data)
