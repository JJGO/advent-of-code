from collections import defaultdict
from parse import parse
import numpy as np


def parses(input):
    nights = []
    start = None
    for line in sorted(input.strip().split("\n")):
        v = parse("[{} {}:{min:d}] {action}", line).named
        if "Guard" in v["action"]:
            v = parse("Guard #{id:d} begins shift", v["action"])
            nights.append([v["id"], []])
        elif "falls" in v["action"]:
            start = v["min"]
        else:
            nights[-1][-1].append((start, v["min"]))
    return nights


def partA(nights):
    # Which guard sleeps the most?
    guards = defaultdict(int)
    for g, vals in nights:
        guards[g] += sum(end - start for start, end in vals)
    gid = max(guards, key=guards.get)
    # for that guard, break down by minute and do argmax
    minutes = np.zeros(60)
    for g, vals in nights:
        if g == gid:
            for start, end in vals:
                minutes[start:end] += 1
    m = np.argmax(minutes)
    return gid * m


def partB(nights):
    # Compute times asleep for each minute as array for each guard
    minutes = defaultdict(lambda: np.zeros(60))
    for g, vals in nights:
        for start, end in vals:
            minutes[g][start:end] += 1
    # Compute (max times asleep, minute when happened) for each guard
    minute = {(g, np.argmax(v)): np.max(v) for g, v in minutes.items()}
    # argmax to get gid and minute value
    gid, m = max(minute, key=minute.get)
    return m * gid


sample = parses(
    """[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up"""
)

if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2018, day=4)
    data = parses(puzzle.input_data)
    assert partA(sample) == 240
    puzzle.answer_a = partA(data)
    assert partB(sample) == 4455
    puzzle.answer_b = partB(data)
