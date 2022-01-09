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


def parse(filename: str) -> IntCode:
    matrix = []
    with open(filename, "r") as f:
        lines = f.read().strip().replace("\n", "")

    l = [int(x) for x in lines.split(",")]

    d = {i: l[i] for i in range(len(l))}
    return IntCode(d)


def pprint(grid):
    # grid = deepcopy(grid)
    # if oxygen:
    #     for i, j in oxygen:
    #         grid[i][j] = 3
    #
    # match = {float("inf"): "#", 0: "S", 1: ".", 2: "T", 3: "O"}
    for row in grid:
        # new_row = [match[el] for el in row]
        print("".join(row))

def get_neighbors_vals(
    matrix: List[List[Union[int, float]]], i: int, j: int, walls_only = True
) -> Generator[Tuple[Tuple[int, int], Union[int, float]], None, None]:
    neighbors = []

    num_rows = len(matrix)
    num_cols = len(matrix[i])

    if i - 1 >= 0:
        neighbors.append((i - 1, j))
    if i + 1 < num_rows:
        neighbors.append((i + 1, j))
    if j - 1 >= 0:
        neighbors.append((i, j - 1))
    if j + 1 < num_cols:
        neighbors.append((i, j + 1))

    if walls_only:
        yield from (
            ((x, y), matrix[x][y])
            for (x, y) in neighbors
            if matrix[x][y] == "#"
        )
    else:
        yield from (
            ((x, y), matrix[x][y])
            for (x, y) in neighbors
        )


def create_grid(intcode) -> List[List[str]]:
    intcode.run()
    grid_s = [chr(i) for i in intcode.outs]
    matrix = "".join(grid_s).strip().split("\n")
    print(f"Matrix:\n{''.join(grid_s)}")

    # for i, row in enumerate(matrix):
    #     matrix[i] = list(row)
    # pprint(matrix)
    return matrix


def find_scaffold_positions(matrix):
    scaffold_pos = []
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == "#":
                neighbors = list(get_neighbors_vals(matrix, i, j, walls_only=True))
                if len(list(get_neighbors_vals(matrix, i, j, walls_only=True))) == 4:
                    scaffold_pos.append((i, j))
    return scaffold_pos

def str_to_cmd(string):
    cmd = [ord(i) for i in string]
    return cmd



def run_program(intcode):

    grid: List[List[str]] = create_grid(intcode)
    scaffold = find_scaffold_positions(grid)
    alignment_sum = sum([x * y for x, y in scaffold])
    return alignment_sum

def run_program_2(intcode):
    intcode.addr[0] = 2
    intcode.inputs.extend(str_to_cmd("A,L,B,L,\n"))
    grid: List[List[str]] = create_grid(intcode)
    return alignment_sum


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None
    intcode = parse(filename)
    run_program(intcode)
    print(f"p1: {answer_a}")
    #p2
    intcode = parse(filename)
    run_program_2(intcode)
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
    # try:
    #     submit_answer(answer_a, "a", day=15, year=2019)
    # except AocdError:
    #     submit_answer(answer_b, "b", day=15, year=2019)
