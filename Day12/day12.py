from collections import Counter, defaultdict, deque
from functools import reduce, lru_cache
from itertools import permutations, combinations
from typing import (
    List,
    Tuple,
    Set,
    Dict,
    Iterable,
    DefaultDict,
    Optional,
    Union,
    Generator,
)
from copy import deepcopy
import re
from math import lcm

from intcode import IntCode


class Moon:
    def __init__(self, id, position: List):
        self.id = id
        self.pos = position
        self.v = [0, 0, 0]

    def __repr__(self):
        return f"Moon with id {self.id}..-Pos:{self.pos}-Velocity:{self.v}"


def parse(filename: str) -> IntCode:
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")

    moons = []
    for i, line in enumerate(lines):
        pos = list(map(int, re.findall("-?\d+", line)))
        moons.append(Moon(i, pos))
    return moons


def move(moon):
    for i, v in enumerate(moon.v):
        moon.pos[i] += v


def moon_energy(moon):
    potential = sum([abs(pos) for pos in moon.pos])
    kinetic = sum([abs(v) for v in moon.v])
    return potential * kinetic


def step(moons):
    for moon1, moon2 in combinations(moons, 2):
        for i, (axis_pos_1, axis_pos_2) in enumerate(list(zip(moon1.pos, moon2.pos))):
            if axis_pos_1 < axis_pos_2:
                moon1.v[i] += 1
                moon2.v[i] -= 1
            elif axis_pos_1 > axis_pos_2:
                moon1.v[i] -= 1
                moon2.v[i] += 1
    # New positions
    [move(moon) for moon in moons]


def run(moons, n_steps):
    for _ in range(n_steps):
        step(moons)
    energy = sum(moon_energy(moon) for moon in moons)
    return energy


def get_state_by_axis(moons):
    axis = [[] for _ in range(3)]

    for i in range(3):
        for moon in moons:
            axis[i].extend([moon.pos[i], moon.v[i]])
    return axis


def run2(moons):
    axis_periods = [None for _ in range(3)]
    initial_state = get_state_by_axis(moons)

    n_step = 1
    while not all([period is not None and n_step != 1 for period in axis_periods]):
        step(moons)
        new_state = get_state_by_axis(moons)
        for i, (initial, new) in enumerate(zip(initial_state, new_state)):
            if initial == new and not axis_periods[i]:
                axis_periods[i] = n_step
        n_step += 1

    out = lcm(*axis_periods)
    return out


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None
    moons = parse(filename)
    n_steps = 100 if "sample" in filename else 1000
    answer_a = run(moons, n_steps)
    #p2
    moons = parse(filename)
    answer_b = run2(moons)
    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 1940
    sample_b_answer = 4686774924

    answer_a, answer_b = main(sample)
    assert (
        answer_a == sample_a_answer
    ), f"AnswerA incorrect: Actual: {answer_a}, Expected: {sample_a_answer}"
    print("sampleA correct")
    if answer_b:
        assert (
            answer_b == sample_b_answer
        ), f"AnswerB incorrect: Actual: {answer_b}, Expected: {sample_b_answer}"
        print("sampleB correct")

    # Test on your input and submit
    answer_a, answer_b = main(input)
    print(f"Your input answers: \nA: {answer_a}\nB: {answer_b}")
    try:
        submit_answer(answer_a, "a", day=12, year=2019)
    except AocdError:
        submit_answer(answer_b, "b", day=12, year=2019)
