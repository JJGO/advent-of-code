import itertools
from functools import lru_cache
import numpy as np


def parses(text):
    scanners = text.strip().split("\n\n")
    scanners = [
        [[int(i) for i in line.split(",")] for line in scanner.split("\n")[1:]]
        for scanner in scanners
    ]
    return [np.array(s) for s in scanners]


@lru_cache()
def righthand_rotations():
    # Generate all 3! * 2**3 possible rotation/mirror matrices
    # and keep the ones that are rotation since det(R) = 1
    # Returns pairs of row permutation indices and signs, not matrices
    I = np.eye(3, dtype=int)
    row_perms = map(np.array, itertools.permutations(range(3)))
    signs = map(np.array, itertools.product((1, -1), repeat=3))
    return [
        (p, s)
        for p, s in itertools.product(row_perms, signs)
        if np.linalg.det(I[p] * s) == 1
    ]


def valid_overlap(known, candidate):
    # known is absolute coordinates, candidate is relative/distances
    for (perm, sign) in righthand_rotations():
        rot_candidate = candidate[:, perm] * sign
        # known = candidate + loc_candidate, so by substracting we get a 2d array of vectors
        # containing the location of candidate if the i^th beacon matched the j^th distance
        pred_locations = known[:, None, :] - rot_candidate[None, :, :]
        loc, counts = np.unique(
            pred_locations.reshape(-1, 3), axis=0, return_counts=True
        )
        candidate_loc = loc[counts >= 12]
        if len(candidate_loc) > 0:
            candidate_loc = candidate_loc[0]
            return candidate_loc, rot_candidate + candidate_loc


def find_absolute_positions(scanners):

    locations = {0: np.array([0,0,0])}
    absolute = {0: scanners[0]}
    unsolved = set(range(1,len(scanners)))
    tested = set()

    while len(unsolved) > 0:
        for known, candidate in itertools.product(absolute, unsolved):
            if (known, candidate) not in tested:
                tested.add((known, candidate))
                if (sol := valid_overlap(absolute[known], scanners[candidate])) is not None:
                    locations[candidate], absolute[candidate] = sol
                    unsolved.remove(candidate)
                    break
    return locations, absolute


def solve_a(scanners):
    _, absolute = find_absolute_positions(scanners)
    return len(np.unique(np.vstack(list(absolute.values())), axis=0))


def solve_b(scanners):
    locations, _ = find_absolute_positions(scanners)
    return max(abs(i - j).sum() for i, j in itertools.combinations(locations.values(), 2))


sample = parses(
    """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14"""
)


if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2021, day=19)
    data = parses(puzzle.input_data)

    assert solve_a(sample) == 79
    puzzle.answer_a = solve_a(data)

    assert solve_b(sample) == 3621
    puzzle.answer_b = solve_b(data)
