from collections import Counter, defaultdict, deque
from functools import reduce, lru_cache
from itertools import product
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

TOTAL_VALID = 0
VALID = set()

def parse(filename: str):
        return 387638, 919123


def generate_trees(l, idx, max_len, min_val, max_val):
    global TOTAL_VALID
    if l:
        min_val_at_k, max_val_at_k = int("".join(list(str(min_val))[:idx])), int("".join(list(str(max_val))[:idx]))

        curr_num = int("".join(l))
        if curr_num < min_val_at_k or curr_num > max_val_at_k:
            return

        if idx == max_len:
            counter = Counter(l)
            if max(counter.values()) < 2:
                return

            if 2 not in counter.values():
                return

            TOTAL_VALID += 1
            VALID.add(int("".join(l)))
            return
    start = str(min_val)[0] if idx == 0 else l[-1]
    for i in range(int(start), 10):
        generate_trees(l[:] + [str(i)], idx + 1, max_len, min_val, max_val)


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    min_val, max_val = parse(filename)
    # ver_count, end_idx, val = parse_string(s, 0, 0)
    generate_trees(list(), idx=0, max_len=6, min_val=min_val, max_val=max_val)
    # init_positions = parse(filename)
    # answer_b = find_gravity(init_positions)
    answer_a = TOTAL_VALID
    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample1.txt"
    input = "input.txt"

    # sample_a_answer = 6
    # sample_b_answer = 50346
    #
    # answer_a, answer_b = main(sample)
    # assert (
    #     answer_a == sample_a_answer
    # ), f"AnswerA incorrect: Actual: {answer_a}, Expected: {sample_a_answer}"
    # print("sampleA correct")
    # # if answer_b:
    # #     assert (
    # #         answer_b == sample_b_answer
    # #     ), f"AnswerB incorrect: Actual: {answer_b}, Expected: {sample_b_answer}"
    # #     print("sampleB correct")
    #
    # # Test on your input and submit
    answer_a, answer_b = main(input)
    # print(f"Your input answers: \nA: {answer_a}\nB: {answer_b}")
    # try:
    #     submit_answer(answer_a, "a", day=3, year=2019)
    # except AocdError:
    #     submit_answer(answer_b, "b", day=3, year=2019)

