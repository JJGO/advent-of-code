from dataclasses import dataclass
from typing import Tuple
import parse


def parse_line(line):
    fmt = "{units:d} units each with {hp:d} hit points{conditions}with an attack that does {attack:d} {damage} damage at initiative {initiative:d}"
    parsed = parse.parse(fmt, line).named
    for condition in parsed.pop("conditions").strip("() ").split("; "):
        if condition != "":
            kind, states = condition.split(" to ")
            states = states.split(", ")
            parsed[kind] = tuple(states)
    return parsed


def parses(data):
    armies = data.split("\n\n")
    armies = [[parse_line(line) for line in army.split("\n")[1:]] for army in armies]
    return armies


@dataclass
class Group:
    units: int
    hp: int
    attack: int
    damage: str
    initiative: int
    idx: int
    army: str = ""
    weak: Tuple[str, ...] = tuple()
    immune: Tuple[str, ...] = tuple()

    def __repr__(self):
        return f"{self.army.title()}({self.idx})"

    def __hash__(self):
        return hash((self.army, self.idx))

    @property
    def power(self):
        return self.units * self.attack

    def damage_to(self, other):
        if self.army == other.army:
            return 0
        if self.damage in other.immune:
            return 0
        dmg = self.power
        if self.damage in other.weak:
            dmg *= 2
        return dmg

    def selection_order(self):
        return (self.power, self.initiative)

    def target_order(self, other):
        return (self.damage_to(other), other.power, other.initiative)

    def attack_order(self):
        return self.initiative

    def deal_damage(self, other):
        if self.units > 0 and other.units > 0:
            dmg = self.damage_to(other)
            other.units = max(0, other.units - dmg // other.hp)


def combat(data, immune_boost=0):
    army1, army2 = data
    immune = [Group(**vals, army="immune", idx=i + 1) for i, vals in enumerate(army1)]
    infection = [
        Group(**vals, army="infection", idx=i + 1) for i, vals in enumerate(army2)
    ]

    for grp in immune:
        grp.attack += immune_boost

    while len(immune) != 0 and len(infection) != 0:
        before_units = [grp.units for grp in immune + infection]
        # Target selection
        targeting = {}
        targeted = set()
        enemies = {"immune": infection, "infection": immune}

        for grp in sorted(infection + immune, reverse=True, key=Group.selection_order):
            targets = [x for x in enemies[grp.army] if x not in targeted]
            if targets:
                target = max(targets, key=grp.target_order)
                if grp.damage_to(target) > 0:
                    targeting[grp] = target
                    targeted.add(target)

        # Combat
        for grp in sorted(infection + immune, reverse=True, key=Group.attack_order):
            if target := targeting.get(grp, None):
                grp.deal_damage(target)

        # Remove dead units
        immune = [grp for grp in immune if grp.units > 0]
        infection = [grp for grp in infection if grp.units > 0]

        # Check stalemate
        after_units = [grp.units for grp in immune + infection]
        if before_units == after_units:
            break

    return immune, infection


def solve_a(data):
    immune, infection = combat(data)
    return sum(grp.units for grp in immune + infection)


def solve_b(data):
    left, right = 0, 10_000
    while right - left > 1:
        mid = (left + right) // 2
        immune, infection = combat(data, mid)
        if len(infection) > 0:
            left = mid
        else:
            right = mid
    immune, infection = combat(data, right)
    return sum(grp.units for grp in immune)


sample = parses(
    """Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4"""
)

if __name__ == "__main__":
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2018, day=24)
    data = parses(puzzle.input_data)

    assert solve_a(sample) == 5216
    puzzle.answer_a = solve_a(data)
    assert solve_b(sample) == 51
    puzzle.answer_b = solve_b(data)
