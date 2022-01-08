from collections import Counter, defaultdict, deque
from functools import reduce, lru_cache
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

def parse(filename: str) -> List[List[int]]:
    matrix = []
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")

    return list(map(int, lines))

def calc_fuel(masses: List[int], p2=False):
    if not p2:
        return sum([x // 3 - 2 for x in masses])
    else:
        return sum([calc_single_fuel(mass) for mass in masses])

def calc_single_fuel(mass):
    fuel = mass // 3 - 2
    if fuel <= 0:
        return 0
    else:
        return fuel + calc_single_fuel(fuel)

def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    masses = parse(filename)
    # ver_count, end_idx, val = parse_string(s, 0, 0)
    answer_a = calc_fuel(masses)
    answer_b = calc_fuel(masses, p2=True)
    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 33583
    sample_b_answer = 50346

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
        submit_answer(answer_a, "a", day=1, year=2019)
    except AocdError:
        submit_answer(answer_b, "b", day=1, year=2019)