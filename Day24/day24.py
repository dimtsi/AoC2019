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


def parse(filename: str):
    matrix = []
    with open(filename, "r") as f:
        lines = f.read().split("\n")

    matrix = [list(line) for line in lines]

    bug_locations = set()
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == "#":
                bug_locations.add((i, j))
    return matrix, bug_locations


def pprint(grid):
    for row in grid:
        print("".join(row))


def pprint_by_level(bug_locations):
    min_level = min(bug_locations, key=lambda x: x[1])[1]
    max_level = max(bug_locations, key=lambda x: x[1])[1]
    
    for level in range(min_level, max_level + 1):
        print(f"level{level}:")
        new_matrix = [["." for _ in range(5)] for _ in range(5)]
        
        filtered_keys = filter(lambda x: x[1] == level, bug_locations)
        for (i, j), _ in filtered_keys:
            new_matrix[i][j] = "#"
        pprint(new_matrix)
        print("\n")


def count_neighbor_bugs(
    matrix: List[List[str]], i: int, j: int
) -> int:
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

    return len(
            [(x, y) for (x, y) in neighbors if matrix[x][y] == "#"]
    )


def step(matrix, curr_bug_locations):
    new_bug_locations = set(curr_bug_locations)
    to_remove = set()
    new_matrix = [["." for _ in range(len(matrix[0]))] for _ in range(len(matrix))]

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            neigh_bugs = count_neighbor_bugs(matrix, i, j)
            if matrix[i][j] == "#":
                if not neigh_bugs == 1:
                    to_remove.add((i, j))
            else:
                if neigh_bugs in {1, 2}:
                    new_bug_locations.add((i, j))

    new_bug_locations -= to_remove
    for i, j in new_bug_locations:
        new_matrix[i][j] = "#"
    return new_matrix, tuple(new_bug_locations)


def biodiv(bug_locations):
    total = 0
    for x, y in bug_locations:
        total += 2 ** ((x * 5) + y)
    return total


def run(matrix, bug_locations):
    history = set()

    history.add(tuple(bug_locations))
    count = 0
    while True:
        print(f"iter: {count}")
        pprint(matrix)
        print()
        new_matrix, new_bug_locations = step(matrix, bug_locations)
        if new_bug_locations in history:
            return biodiv(new_bug_locations)
        history.add(new_bug_locations)
        matrix = deepcopy(new_matrix)
        bug_locations = new_bug_locations
        count += 1


def count_neighbor_bugs_p2(
    i: int, j: int, level, bugs: Dict) -> int:
    neighbors = []

    num_rows = 5
    num_cols = 5

    if i - 1 >= 0:
        if (i - 1, j) != (2, 2):
            neighbors.append(((i - 1, j), level))
        else:
            [neighbors.append(((4, jj), level + 1)) for jj in range(5)]
    else:
        neighbors.append(((1, 2), level - 1))

    if i + 1 < num_rows:
        if (i + 1, j) != (2, 2):
            neighbors.append(((i + 1, j), level))
        else:
            [neighbors.append(((0, jj), level + 1)) for jj in range(5)]
    else:
        neighbors.append(((3, 2), level - 1))

    if j - 1 >= 0:
        if (i, j - 1) != (2, 2):
            neighbors.append(((i, j - 1), level))
        else:
            [neighbors.append(((ii, 4), level + 1)) for ii in range(5)]
    else:
        neighbors.append(((2, 1), level - 1))

    if j + 1 < num_cols:
        if (i, j + 1) != (2, 2):
            neighbors.append(((i, j + 1), level))
        else:
            [neighbors.append(((ii, 0), level + 1)) for ii in range(5)]
    else:
        neighbors.append(((2, 3), level - 1))

    return len(
            [((x, y), lev) for ((x, y), lev) in neighbors if ((x, y), lev) in bugs]
    )


def step_p2(curr_bug_locations):
    new_bug_locations = set(curr_bug_locations)
    to_remove = set()
    
    min_level = min(curr_bug_locations, key=lambda x: x[1])[1]
    max_level = max(curr_bug_locations, key=lambda x: x[1])[1]
    
    for level in list(range(min_level - 1, max_level + 2)):
        for i in range(5):
            for j in range(5):
                if (i, j) == (2, 2):
                    continue
                neigh_bugs = count_neighbor_bugs_p2(i, j, level, curr_bug_locations)
                if ((i, j), level) in curr_bug_locations:
                    if not neigh_bugs == 1:
                        to_remove.add(((i, j), level))
                else:
                    if neigh_bugs in {1, 2}:
                        new_bug_locations.add(((i, j), level))

        new_bug_locations -= to_remove
    return new_bug_locations


def run_p2(bug_locations, n_steps):

    count = 0
    bug_locations = set([(pos, 0) for pos in bug_locations])

    while count < n_steps:
        bug_locations = step_p2(bug_locations)
        count += 1
        # print(f"iter: {count}")
        # pprint_by_level(bug_locations)
        # print()
    return len(bug_locations)


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None
    grid, bug_locations = parse(filename)
    answer_a = run(grid, bug_locations)
    print(f"p1: {answer_a}")

    # #p2
    grid, bug_locations = parse(filename)

    n_steps = 10 if "sample" in filename else 200
    answer_b = run_p2(bug_locations, n_steps)
    print(f"p2: {answer_b}")
    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    inp = "input.txt"

    sample_a_answer = 2129920
    sample_b_answer = 99

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
    answer_a, answer_b = main(inp)
    print(f"Your input answers: \nA: {answer_a}\nB: {answer_b}")
    try:
        submit_answer(answer_a, "a", day=24, year=2019)
    except AocdError:
        submit_answer(answer_b, "b", day=24, year=2019)
