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
from heapq import heappop, heappush
from time import sleep

from intcode import IntCode
from termcolor import colored

UP, DOWN, LEFT, RIGHT = range(1, 5)
BACKTR = {UP: DOWN, LEFT: RIGHT, RIGHT: LEFT, DOWN: UP}

TEST_GRID = """
#######...#####
#.....#...#...#
#.....#...#...#
......#...#...#
......#...###.#
......#.....#.#
^########...#.#
......#.#...#.#
......#########
........#...#..
....#########..
....#...#......
....#...#......
....#...#......
....#####......
""".strip().split("\n")


def parse(filename: str) -> IntCode:
    matrix = []
    with open(filename, "r") as f:
        lines = f.read().strip().replace("\n", "")

    l = [int(x) for x in lines.split(",")]

    d = {i: l[i] for i in range(len(l))}
    return IntCode(d)


def check(intcode, i, j):
    intcode.inputs.extend([i, j])
    intcode.run()
    intcode.reset()
    return intcode.outs[-1]


def run_program(intcode):
    count = 0
    for i in range(50):
        for j in range(50):
            if check(intcode, i, j) == 1:
                count += 1
    return count


def create_grid(intcode):
    grid = []
    for i in range(100):
        row = [None for _ in range(100)]
        for j in range(100):
            intcode.inputs.extend([i, j])
            intcode.run()
            intcode.reset()
            if intcode.outs[-1] == 1:
                row[j] = "#"
            else:
                row[j] = "."
        grid.append(row[:])
    import pickle
    pickle.dump(grid, open("grid.pkl", "wb"))

    for row in grid:
        print("".join(row))
    print()

def pprint(grid):
    for row in grid:
        print("".join(row))


def run_program_2(intcode):

    i = j = 0
    while not check(intcode, i + 99, j):
        j += 1
        while not check(intcode, i, j + 99):
            i += 1

    return i * 10000 + j




def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None
    intcode = parse(filename)
    answer_a = run_program(intcode)
    print(f"p1: {answer_a}")
    # p2
    intcode = parse(filename)
    answer_b = run_program_2(intcode)
    # print(f"p2: {answer_b}")
    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":
    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    inp = "input.txt"

    # sample_a_answer = 1125899906842624
    # sample_b_answer = 18216
    #
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
    answer_a, answer_b = main(inp)
    print(f"Your input answers: \nA: {answer_a}\nB: {answer_b}")
    try:
        submit_answer(answer_a, "a", day=19, year=2019)
    except AocdError:
        submit_answer(answer_b, "b", day=19, year=2019)
