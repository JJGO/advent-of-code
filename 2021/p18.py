import itertools
import json
import operator
from dataclasses import dataclass
from functools import reduce
from typing import Union


def parses(text):
    return [json.loads(line) for line in text.strip().split("\n")]


@dataclass
class SN:
    left: Union["SN", int]
    right: Union["SN", int]

    def __repr__(self):
        return f"[{repr(self.left)},{repr(self.right)}]"

    @staticmethod
    def fromlist(data):
        l, r = data
        left = l if isinstance(l, int) else SN.fromlist(l)
        right = r if isinstance(r, int) else SN.fromlist(r)
        return SN(left, right)

    def __add__(self, other):
        return SN(self, other).reduce()

    def __getitem__(self, pos):
        head, tail = pos[0], pos[1:]
        node = [self.left, self.right][head]
        return node if len(tail) == 0 else node[tail]

    def __setitem__(self, pos, val):
        head, tail = pos[0], pos[1:]
        if len(tail) == 0:
            if head == 0:
                self.left = val
            else:
                self.right = val
        else:
            node = [self.left, self.right][head]
            node[tail] = val

    def find_neighbor(self, pos, side):
        # 0 is left, 1 is right
        if len(pos) == 0:
            return None
        if pos[-1] == 1 - side:
            neighbor = pos[:-1] + (side,)
            while not isinstance(self[neighbor], int):
                neighbor += (1 - side,)
            return neighbor
        return self.find_neighbor(pos[:-1], side)

    def neighbors(self, pos):
        return self.find_neighbor(pos, 0), self.find_neighbor(pos, 1)

    def __iter__(self):
        return iter([self.left, self.right])

    def find_explode(self):
        stack = [(self, tuple())]
        while stack:
            num, pos = stack.pop()
            if len(pos) == 4:
                return pos
            for i, child in enumerate((num.right, num.left)):
                if isinstance(child, SN):
                    stack.append((child, pos + (1 - i,)))

    def find_split(self):
        stack = [(self, tuple())]
        while stack:
            num, pos = stack.pop()
            if isinstance(num, int) and num > 9:
                return pos
            elif isinstance(num, SN):
                for i, child in enumerate((num.right, num.left)):
                    stack.append((child, pos + (1 - i,)))

    def reduce(self):
        while True:
            if pos := self.find_explode():
                pair = (self[pos].left, self[pos].right)
                self[pos] = 0
                for neigh, val in zip(self.neighbors(pos), pair):
                    if neigh is not None:
                        self[neigh] = self[neigh] + val
                continue

            if pos := self.find_split():
                val = self[pos]
                n = val // 2
                self[pos] = SN(n, val - n)
                continue

            break
        return self

    def magnitude(self):
        left = self.left if isinstance(self.left, int) else self.left.magnitude()
        right = self.right if isinstance(self.right, int) else self.right.magnitude()
        return 3 * left + 2 * right


def solve_a(nums):
    return reduce(operator.add, map(SN.fromlist, nums)).magnitude()


def solve_b(nums):
    C = SN.fromlist
    return max(
        (C(a) + C(b)).magnitude()
        for a, b in itertools.product(nums, repeat=2)
        if a != b
    )


sample = parses(
    """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""
)

if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2021, day=18)
    data = parses(puzzle.input_data)

    assert solve_a(sample) == 4140
    puzzle.answer_a = solve_a(data)

    assert solve_b(sample) == 3993
    puzzle.answer_b = solve_b(data)
