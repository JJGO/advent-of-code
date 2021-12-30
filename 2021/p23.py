# Solution is Dijsktra (or preferably A*) in the implicit game graph using energy to order solutions

from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property
from heapq import heappop, heappush
from typing import Dict, Tuple


def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    return 0


@dataclass
class State:
    positions: Dict[Tuple[int, int], str]
    final: Dict[str, Tuple[int, int]]
    energy: int = 0
    maxy: int = 3

    HALLWAY = set([(1, 1), (2, 1), (4, 1), (6, 1), (8, 1), (10, 1), (11, 1)])
    ENERGIES = {"A": 1, "B": 10, "C": 100, "D": 1000}

    def check_collisions(self, start, end):
        c = self.positions[start]
        x, y = start
        x2, y2 = end
        e = 0
        # Move into hallway (if needed)
        while y != 1:
            y -= 1
            if (x, y) in self.positions:
                return None
            e += self.ENERGIES[c]
        # Move along the hallway (if needed)
        while x != x2:
            x += sign(x2 - x)
            if (x, y) in self.positions:
                return None
            e += self.ENERGIES[c]
        # Move into the Room (if needed)
        while y != y2:
            y += sign(y2 - y)
            if (x, y) in self.positions:
                return None
            e += self.ENERGIES[c]
        return e

    def move(self, start, end):
        if end in self.positions:
            return None
        if energy := self.check_collisions(start, end):
            new_positions = self.positions.copy()
            new_final = self.final.copy()
            new_energy = self.energy + energy
            new_positions[end] = new_positions.pop(start)
            # clean if moved into final room
            c = self.positions[start]
            if end == self.final[c]:
                new_positions.pop(end)
                x, y = new_final[c]
                if y == 2:
                    new_final.pop(c)
                else:
                    new_final[c] = (x, y - 1)
            return State(new_positions, new_final, new_energy, self.maxy)

    def all_moves(self, pos):
        c = self.positions[pos]
        # If we can move into final position, it's optimal to do so
        if s := self.move(pos, self.final[c]):
            return [s]
        # We can only choose if we haven't moved into the hallway yet
        possible_moves = []
        if pos not in self.HALLWAY:
            for pos2 in self.HALLWAY:
                if pos2 not in self.positions and (s := self.move(pos, pos2)):
                    possible_moves.append(s)
        return possible_moves

    def children(self):
        return sum([self.all_moves(pos) for pos in self.positions], [])

    def check_initial(self):
        # Move from initial to final positions that already correct
        new_positions = self.positions.copy()
        new_final = self.final.copy()
        for k in range(self.maxy, 1, -1):
            for c, (x, y) in list(new_final.items()):
                if y == k and new_positions.get((x, y), None) == c:
                    new_positions.pop((x, y))
                    if k == 2:
                        new_final.pop(c)
                    else:
                        new_final[c] = (x, k - 1)
        return State(new_positions, new_final, self.energy, self.maxy)

    @staticmethod
    def fromstr(diagram):
        # Parse map into
        initial = {}
        for j, line in enumerate(diagram.strip().split("\n")):
            for i, v in enumerate(line):
                if v in "ABCD":
                    initial[i, j] = v
        maxy = max(j for _, j in initial)
        final = {c: (3 + 2 * i, maxy) for i, c in enumerate("ABCD")}
        return State(initial, final, maxy=maxy).check_initial()

    @cached_property
    def hash(self):
        return hash(tuple([(x, y, c) for (x, y), c in self.positions.items()]))

    def __hash__(self):
        return self.hash

    def __eq__(self, other):
        # Energy is not part of positions, otherwise we'd memoize with energy as well
        # final can be derived from positions
        return self.hash == other.hash

    def done(self):
        return len(self.final) == 0

    def remaining(self):
        return sum(y - 1 for _, y in self.final.values())

    def lower_bound_completion(self):
        final = self.final.copy()
        energy_lb = 0
        for (x, y), c in self.positions.items():
            x2, y2 = final[c]
            movement = abs(y - 1) + abs(y2 - 1) + abs(x - x2)
            energy_lb += movement * self.ENERGIES[c]
            final[c] = (x2, y2 - 1)
        return energy_lb

    @cached_property
    def cost(self):
        return (
            self.energy + self.lower_bound_completion(),
            self.energy,
            self.remaining(),
        )

    def __lt__(self, other):
        return self.cost < other.cost

    def render(self):
        s = ""
        for j in range(self.maxy + 2):
            for i in range(13):
                if (i, j) in self.positions:
                    s += self.positions[i, j]
                elif 2 <= j <= self.maxy and i in [3, 5, 7, 9]:
                    c = "ABCD"[(i - 3) // 2]
                    if c not in self.final or j > self.final[c][1]:
                        s += c
                    else:
                        s += "."
                else:
                    s += "." if j == 1 and 0 < i < 12 else "#"
            s += "\n"
        print(s)


def solve_a(data):
    heap = [State.fromstr(data)]
    visited = defaultdict(lambda: float("inf"))
    while heap:
        state = heappop(heap)
        if state.done():
            return state.energy
        for child in state.children():
            if child.energy < visited[child]:
                visited[child] = child.energy
                heappush(heap, child)


def solve_b(data):
    extra_rows = "  #D#C#B#A#\n  #D#B#A#C#\n"
    data = data[:42] + extra_rows + data[42:]
    return solve_a(data)


sample = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""

if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2021, day=23)
    data = puzzle.input_data

    assert solve_a(sample) == 12521
    puzzle.answer_a = solve_a(data)

    assert solve_b(sample) == 44169
    puzzle.answer_b = solve_b(data)
