from collections import Counter, defaultdict
import numpy as np
from einops import rearrange


def parses(text):
    def parse_arr(s):
        arr = []
        for row in s.split("/"):
            arr.append([v == "#" for v in row])
        return np.array(arr, dtype=np.uint8)

    lines = [line.split(" => ") for line in text.strip().split("\n")]
    return [(parse_arr(i), parse_arr(j)) for i, j in lines]


def transformations(arr):
    # 8 transformations, 4 rotations for each chirality
    orientations = []
    for x in (arr, np.fliplr(arr)):
        for k in range(4):
            orientations.append(np.rot90(x, k))
    return orientations


def rothash(arr):
    # Array hash that's invariant to rotations/flips
    return sum([hash(t.tobytes()) for t in transformations(arr)])


def solve_a(data, steps=5):
    # Rearrange solves the boring rearranging
    mapping = {}
    tile = np.array([[0, 1, 0], [0, 0, 1], [1, 1, 1]], dtype=np.uint8)

    for a, b in data:
        mapping[rothash(a)] = b

    for _ in range(steps):
        N = len(tile)
        k = 2 if N % 2 == 0 else 3
        tiles = rearrange(tile, "(h h1) (w w1) -> h w h1 w1", h1=k, w1=k)
        transformed_tiles = np.array(
            [[mapping[rothash(tile)] for tile in row] for row in tiles]
        )
        tile = rearrange(transformed_tiles, "h w h1 w1 -> (h h1) (w w1)")

    return tile.sum()


def solve_b(data, steps=18):
    # full tile size follows the progression (considering only a single side)
    # 3, 2*2, 2*3, 3*3, ..., 3**n, 2*3**(n-1), 2*3**n, 3**(n+1), ...
    # so we can group steps in groups of three where each 3x3 tile generates 9 3x3 tiles
    # that won't interact in the future with the rest of the mosaic.
    # We can thus precompute the 3x3 -> 9 3x3 mapping using rothashes and ignore actual tiles
    assert steps % 3 == 0
    mapping = {}

    for a, b in data:
        mapping[rothash(a)] = b

    counts = {}
    sums = {}
    for tile, _ in data:
        if tile.shape == (3, 3):
            sums[rothash(tile)] = int(tile.sum())
            tile_4x4 = mapping[rothash(tile)]
            tiles_4_2x2 = rearrange(tile_4x4, "(h h1) (w w1) -> h w h1 w1", h1=2, w1=2)
            tiles_4_3x3 = np.array(
                [[mapping[rothash(tile)] for tile in row] for row in tiles_4_2x2]
            )
            tile_6x6 = rearrange(tiles_4_3x3, "h w h1 w1 -> (h h1) (w w1)")
            tiles_9_2x2 = rearrange(tile_6x6, "(h h1) (w w1) -> h w h1 w1", h1=2, w1=2)
            tiles_9_3x3 = np.array(
                [[mapping[rothash(tile)] for tile in row] for row in tiles_9_2x2]
            )
            counts[rothash(tile)] = Counter(
                [rothash(t) for t in tiles_9_3x3.reshape(-1, 3, 3)]
            )

    tile = np.array([[0, 1, 0], [0, 0, 1], [1, 1, 1]], dtype=np.uint8)
    state = {rothash(tile): 1}
    for _ in range(steps // 3):
        new_state = defaultdict(int)
        for tile, n in state.items():
            for new_tile, m in counts[tile].items():
                new_state[new_tile] += n * m
        state = new_state
    return sum([sums[t] * n for t, n in state.items()])


sample = parses(
    """../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#"""
)

if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2017, day=21)
    data = parses(puzzle.input_data)

    assert solve_a(sample, 2) == 12
    puzzle.answer_a = solve_a(data)

    assert solve_a(data, 6) == solve_b(data, 6)
    puzzle.answer_b = solve_b(data)
