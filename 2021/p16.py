import math
from dataclasses import dataclass
from typing import Sequence


def list2num(nums):
    return sum(2**i * n for i, n in enumerate(reversed(nums)))


@dataclass
class Packet:
    version: int
    type_: int


@dataclass
class Literal(Packet):
    value: int

    def sum_versions(self) -> int:
        return self.version


@dataclass
class Operator(Packet):
    subpackets: Sequence[Packet]

    OP_FN = {
        0: sum,
        1: math.prod,
        2: min,
        3: max,
        5: lambda x: int(x[0] > x[1]),
        6: lambda x: int(x[0] < x[1]),
        7: lambda x: int(x[0] == x[1]),
    }

    def sum_versions(self) -> int:
        return self.version + sum(s.sum_versions() for s in self.subpackets)

    @property
    def value(self) -> int:
        return self.OP_FN[self.type_]([s.value for s in self.subpackets])


class Buffer:
    def __init__(self, data):
        self.p = 0
        bytes_ = [int(h, 16) for h in data.strip()]
        self.bits = [int(h & i > 0) for h in bytes_ for i in [8, 4, 2, 1]]

    def read(self, n) -> int:
        bits = self.bits[self.p : self.p + n]
        self.p += n
        return list2num(bits)

    def read_literal(self) -> int:
        b, n = 1, 0
        while b == 1:
            b = self.read(1)
            n = (n << 4) | self.read(4)
        return n

    def decode(self) -> "Packet":
        version = self.read(3)
        type_ = self.read(3)
        if type_ == 4:
            val = self.read_literal()
            return Literal(version, type_, val)

        length = self.read(1)
        if length == 0:
            end = self.read(15) + self.p  # order is critical here
            subpackets = []
            while self.p < end:
                subpackets.append(self.decode())
        else:
            subpackets = [self.decode() for _ in range(self.read(11))]
        return Operator(version, type_, subpackets)


def solve_a(data):
    return Buffer(data).decode().sum_versions()


def solve_b(data):
    return Buffer(data).decode().value


samples_a = [
    ("8A004A801A8002F478", 16),
    ("620080001611562C8802118E34", 12),
    ("C0015000016115A2E0802F182340", 23),
    ("A0016C880162017C3686B18A3D4780", 31),
]

samples_b = [
    ("C200B40A82", 3),
    ("04005AC33890", 54),
    ("880086C3E88112", 7),
    ("CE00C43D881120", 9),
    ("D8005AC2A8F0", 1),
    ("F600BC2D8F", 0),
    ("9C005AC2F8F0", 0),
    ("9C0141080250320F1802104A08", 1),
]

if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2021, day=16)
    data = puzzle.input_data

    for sample, sol in samples_a:
        assert solve_a(sample) == sol
    puzzle.answer_a = solve_a(data)

    for sample, sol in samples_b:
        assert solve_b(sample) == sol
    puzzle.answer_b = solve_b(data)
