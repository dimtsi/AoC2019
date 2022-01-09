from collections import Counter, defaultdict, deque
from functools import reduce, lru_cache
from itertools import permutations, combinations, product
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
from math import ceil, floor


def parse(filename: str):
    with open(filename, "r") as f:
        inp = [int(x) for x in f.read().strip()]
    return inp


def get_patterns(base_pattern, size):
    patterns = []
    for i in range(size):
        base = []
        for j in base_pattern:
            base.extend([j] * (i + 1))
        idx = 0
        pattern = [None for _ in range(size)]
        base_idx = 1
        while idx < size:
            pattern[idx] = base[base_idx % len(base)]
            idx += 1
            base_idx += 1
        patterns.append(pattern)
    return patterns


def run(inp_l, n_steps, p2=False):
    size = len(inp_l)
    offset = int("".join(map(str, inp_l[:7])))
    offset_to_end = size - offset
    if not p2:
        patterns = get_patterns([0, 1, 0, -1], size)
        print()

        for _ in range(n_steps):
            new_l = []
            for pattern in patterns:
                sum_prod = sum([x * y for (x, y) in zip(inp_l, pattern)])
                new_l.append(abs(sum_prod) % 10)
            inp_l = new_l
        return int("".join([str(x) for x in inp_l[:8]]))

    else:
        # only 1s upper-triangular
        inp_l = inp_l[offset:]
        size = len(inp_l)
        assert offset_to_end == size, f"{offset_to_end}, {size}"
        assert offset_to_end < offset  # for only 1s to hold
        
        for i in range(n_steps):
            new_l = [None for _ in range(size)]
            total = sum(inp_l)
            new_l[0] = total % 10
            for j in range(1, len(inp_l)):
                total -= inp_l[j - 1]
                new_l[j] = total % 10
            inp_l = new_l[:]
        return int("".join([str(x) for x in inp_l[:8]]))

                
                



        



def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    inp_list = parse(filename)
    answer_a = run(inp_list, 100)

    if "sample" in filename:
        filename = "sample2.txt"
    inp_list = parse(filename)
    answer_b = run(inp_list * 10000, 100, p2=True)
    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 52432133
    sample_b_answer = 53553731

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
        submit_answer(answer_a, "a", day=16, year=2019)
    except AocdError:
        submit_answer(answer_b, "b", day=16, year=2019)
