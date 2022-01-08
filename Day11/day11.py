from collections import Counter, defaultdict, deque
from functools import reduce, lru_cache
from itertools import permutations
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

from intcode import IntCode


def parse(filename: str) -> IntCode:
    matrix = []
    with open(filename, "r") as f:
        lines = f.read().strip().replace("\n", "")

    l = [int(x) for x in lines.split(",")]

    d = {i: l[i] for i in range(len(l))}
    return IntCode(d)


def left(dir):
    if dir == "^":
        return "<"
    if dir == "<":
        return "v"
    if dir == "v":
        return ">"
    if dir == ">":
        return "^"


def right(dir):
    if dir == "^":
        return ">"
    if dir == "<":
        return "^"
    if dir == "v":
        return "<"
    if dir == ">":
        return "v"


def new_pos(pos, dir):
    i, j = pos
    if dir == "^":
        return (i - 1, j)
    if dir == "<":
        return (i, j - 1)
    if dir == "v":
        return (i + 1, j)
    if dir == ">":
        return (i, j + 1)


def pprint(panel):
    min_x = min(panel, key=lambda x: x[0])[0]
    max_x = max(panel, key=lambda x: x[0])[0]
    min_y = min(panel, key=lambda x: x[1])[1]
    max_y = max(panel, key=lambda x: x[1])[1]

    range_x = max_x - min_x
    range_y = max_y - min_y

    output = [[" " for _ in range(range_y + 1)] for _ in range(range_x + 1)]

    for (x, y), color in panel.items():
        target_x = x - min_x
        target_y = y - min_y

        if color == 1:
            output[target_x][target_y] = "#"

    for row in output:
        print("".join(row))


def run_program(intcode: IntCode, p2=False):
    panel = defaultdict(lambda: 0)
    panel[(0, 0)] = 0 if not p2 else 1
    curr_pos = (0, 0)
    curr_dir = "^"

    has_been_painted = set()

    while not intcode.is_halted:
        curr_col = panel[curr_pos]
        intcode.inputs.extend([curr_col])
        intcode.run()
        out_col, out_dir = intcode.outs[-2], intcode.outs[-1]

        if out_col != curr_col:
            has_been_painted.add(curr_pos)
            panel[curr_pos] = out_col
        new_dir = left(curr_dir) if out_dir == 0 else right(curr_dir)
        curr_pos = new_pos(curr_pos, new_dir)
        curr_dir = new_dir

    if p2:
        pprint(panel)
    return len(has_been_painted)


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None
    intcode = parse(filename)
    answer_a = run_program(intcode)
    print(f"p1: {answer_a}")
    # #p2
    intcode = parse(filename)
    run_program(intcode, p2=True)
    print(f"p2: {answer_b}")
    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    # sample_a_answer = 1125899906842624
    # sample_b_answer = 18216

    # answer_a, answer_b = main(sample)
    # assert (
    #     answer_a == sample_a_answer
    # ), f"AnswerA incorrect: Actual: {answer_a}, Expected: {sample_a_answer}"
    # print("sampleA correct")
    # if answer_b:
    #     assert (
    #         answer_b == sample_b_answer
    #     ), f"AnswerB incorrect: Actual: {answer_b}, Expected: {sample_b_answer}"
    #     print("sampleB correct")

    # Test on your input and submit
    answer_a, answer_b = main(input)
    # print(f"Your input answers: \nA: {answer_a}\nB: {answer_b}")
    # try:
    #     submit_answer(answer_a, "a", day=7, year=2019)
    # except AocdError:
    #     submit_answer(answer_b, "b", day=7, year=2019)
