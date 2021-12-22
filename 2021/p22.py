import itertools
import math
import re


def parses(text):
    lines = [
        (line.startswith("on"), tuple(int(i) for i in re.findall(r"-?\d+", line)))
        for line in text.strip().split("\n")
    ]
    return [(on, coords[:2], coords[2:4], coords[4:]) for on, coords in lines]


def solve_a(data):
    points = set()
    for on, *ranges in data:
        if all(a >= -50 and b <= 51 for a, b in ranges):
            p = set(itertools.product(*[range(a, b + 1) for (a, b) in ranges]))
            if on:
                points |= p
            else:
                points -= p
    return len(points)


import math


class Rectangle:
    def __init__(self, *intervals, inclusive=False):
        I = int(inclusive)
        self.intervals = tuple((a, b + I) for a, b in intervals)

    @property
    def volume(self):
        return math.prod(b - a for a, b in self.intervals)

    def __eq__(self, other):
        return all(intA == intB for intA, intB in zip(self.intervals, other.intervals))

    def __hash__(self):
        return hash(sum(self.intervals, start=tuple()))

    def __repr__(self):
        if len(self.intervals) == 1:
            return f"{self.__class__.__name__}({self.intervals[0]})"
        return f"{self.__class__.__name__}{self.intervals}"

    def overlap(self, other):
        if other is None:
            return None
        overlap_intervals = []
        for (minA, maxA), (minB, maxB) in zip(self.intervals, other.intervals):
            minC = max(minA, minB)
            maxC = min(maxA, maxB)
            if minC >= maxC:
                return None
            overlap_intervals.append((minC, maxC))
        return Rectangle(*overlap_intervals)

    # returns overlap as Rectangle or None if no overlap
    def __and__(self, other):
        return self.overlap(other)

    def split(self, dim, val):
        left, right = self.intervals[dim]
        assert left < val < right
        split1, split2 = (left, val), (val, right)
        r1 = Rectangle(
            *[
                interval if d != dim else split1
                for d, interval in enumerate(self.intervals)
            ]
        )
        r2 = Rectangle(
            *[
                interval if d != dim else split2
                for d, interval in enumerate(self.intervals)
            ]
        )
        return [r1, r2]

    def substract(self, other):
        overlap = self & other
        if overlap is None:
            return [self]  # no overlap
        elif overlap == self:
            return []  # other covers self
        else:
            # partial cover
            for d, ((minA, maxA), (minB, maxB)) in enumerate(
                zip(self.intervals, other.intervals)
            ):
                if minB > minA:
                    r1, r2 = self.split(d, minB)
                    return [r1] + r2.substract(other)
                elif maxB < maxA:
                    r1, r2 = self.split(d, maxB)
                    return r1.substract(other) + [r2]
        assert False, "Should not reach"

    # returns List[Rectangle] resulting from substracting self to other
    def __sub__(self, other):
        return self.substract(other)

    # return List[Rectangle] representing mutually exclusive partitions from
    # other not contained in self
    def __add__(self, other):
        if overlap := self.overlap(other):
            return other.substract(overlap)
        return [other]


def solve_b(data):
    # Faster solution that only stores mutually exclusive positive regions
    # Relies on Rectangle.split and Rectangle.substract
    # On intersections, it repeatedly splits the N-Rectangle until there are no intersections
    # Since it keeps track of fewer rectn

    rectangles = []
    for on, *ranges in data:
        B = Rectangle(*ranges, inclusive=True)
        if on:
            Bs = [B]
            for A in rectangles:
                Bs = [R for B in Bs for R in B - (A & B)]
            rectangles.extend(Bs)
        else:
            rectangles = [R for A in rectangles for R in A - B]
    return sum(A.volume for A in rectangles)


def solve_b_nosplit(data):
    # Simple solution that only requires Rectangle.overlap and Rectangle.volume
    # We always add new positive regions and then consider all intersections
    # with existing positive and negative regions
    # On intersections with positive regions, we add negative and viceversa
    positive = []
    negative = []

    for on, *ranges in data:
        B = Rectangle(*ranges, inclusive=True)
        new_positive = []
        new_negative = []

        for A in positive:
            if overlap := A & B:
                new_negative.append(overlap)
        for A in negative:
            if overlap := A & B:
                new_positive.append(overlap)
        if on:
            new_positive.append(B)
        positive += new_positive
        negative += new_negative
    return sum(R.volume for R in positive) - sum(R.volume for R in negative)


sample = parses(
    """on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10"""
)

sample2 = parses(
    """on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682"""
)

sample3 = parses(
    """on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2021, day=22)
    data = parses(puzzle.input_data)

    assert solve_a(sample) == 39
    assert solve_a(sample2) == 590784
    assert solve_a(sample3) == 474140
    puzzle.answer_a = solve_a(data)

    assert solve_b(sample3) == 2758514936282235
    puzzle.answer_b = solve_b(data)
    assert solve_b_nosplit(sample3) == 2758514936282235
