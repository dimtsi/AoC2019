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


def parse(filename: str) -> Dict:
    matrix = []
    with open(filename, "r") as f:
        lines = f.read().strip().replace("\n", "")


    l = [int(x) for x in lines.split(",")]

    d = {i: l[i] for i in range(len(l))}
    return d


def run_cmds(pos: Dict, noun, verb):
    i = 0
    pos[1] = noun
    pos[2] = verb
    while pos[i] != 99:
        op = pos[i]
        x, y, z = pos[pos[i + 1]], pos[pos[i + 2]], pos[i + 3]
        if op == 1:
            pos[z] = x + y
        elif op == 2:
            pos[z] = x * y
        if op not in {1, 2, 99}:
            return -1
            # raise Exception("Wrong operation")
        i += 4
    return pos[0]

def find_gravity(init_positions):
    for i in range(100):
        for j in range(100):
            if run_cmds(deepcopy(init_positions), i, j) == 19690720:
                return 100 * i + j
    return None


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    init_positions = parse(filename)
    # ver_count, end_idx, val = parse_string(s, 0, 0)
    answer_a = run_cmds(init_positions, 12, 2)
    init_positions = parse(filename)
    answer_b = find_gravity(init_positions)
    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 5434663
    sample_b_answer = 50346

    answer_a, answer_b = main(sample)
    assert (
        answer_a == sample_a_answer
    ), f"AnswerA incorrect: Actual: {answer_a}, Expected: {sample_a_answer}"
    print("sampleA correct")
    # if answer_b:
    #     assert (
    #         answer_b == sample_b_answer
    #     ), f"AnswerB incorrect: Actual: {answer_b}, Expected: {sample_b_answer}"
    #     print("sampleB correct")

    # Test on your input and submit
    answer_a, answer_b = main(input)
    print(f"Your input answers: \nA: {answer_a}\nB: {answer_b}")
    try:
        submit_answer(answer_a, "a", day=2, year=2019)
    except AocdError:
        submit_answer(answer_b, "b", day=2, year=2019)
