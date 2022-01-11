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
from copy import deepcopy, copy
import re
from heapq import heappop, heappush
from time import sleep

from intcode import IntCode
from termcolor import colored

UP, DOWN, LEFT, RIGHT = range(1, 5)
BACKTR = {UP: DOWN, LEFT: RIGHT, RIGHT: LEFT, DOWN: UP}


def parse(filename: str):
    matrix = []
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")
    all_keys = set()
    for i, line in enumerate(lines):
        for j in range(len(line)):
            if line[j].islower():
                all_keys.add(line[j])
            elif line[j] == "@":
                start = (i, j)


    return [list(line) for line in lines], start, all_keys


class State:
    def __init__(self, pos, found):
        self.pos = pos
        self.found = found

    def __repr__(self):
        return f"State, pos: {self.pos}, found: {self.found}"
    
    def __lt__(self, other):
        return hash(self) < hash(other)

    def __hash__(self):
        return hash(self.pos) + hash(tuple(self.found))


def pprint(grid,):

    for row in grid:
        print("".join(row))


def get_neighbors_vals(
    matrix: List[List[str]], state: State,
) -> Generator[Tuple[Tuple[int, int], str], None, None]:
    (i, j), found = state

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

    yield from (
        ((x, y), matrix[x][y])
        for (x, y) in neighbors
        if not (matrix[x][y] == "#" or (matrix[x][y].isupper() and matrix[x][y].lower() not in found))
    )


def min_cost(matrix, start, all_keys):

    complete = set()
    complete_pos_dist = set()
    min_dist = float("inf")
    start_state = (start, tuple())

    distances = defaultdict(lambda: float("inf"))
    distances[start_state] = 0
    pq = [(0, start_state)]
    visited = set()

    while pq:
        dist, elem = heappop(pq)
        if elem in visited or dist > min_dist:
            continue
        visited.add(elem)
        for (i, j), val in get_neighbors_vals(matrix, elem):

            new_state = ((i, j), elem[1])

            if val.islower():
                new_pos, new_found = new_state
                new_state = ((i, j), tuple(sorted(set(new_found) | set(val))))
            if new_state not in visited or distances[new_state] > dist + 1:
                distances[new_state] = dist + 1
                if val.islower() and len(new_state[1]) == len(all_keys):
                    complete_pos_dist.add((new_state, distances[new_state]))
                    complete.add(distances[new_state])
                    min_dist = min(complete)
                    continue
                if dist + 1 > min_dist:
                    continue
                heappush(pq, (dist + 1, new_state))
    min_dist = min(complete)

    return min_dist


def print_origin(origin, end):
    next_hash = list(end)[0][0]
    y = origin
    path = []

    while next_hash in origin:
        state = origin[next_hash]
        path.append(deepcopy(state))
        next_hash = hash(state)
    print()






def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None
    grid, start_pos, all_keys = parse(filename)
    answer_a = min_cost(grid, start_pos, all_keys)
    print(f"p1: {answer_a}")
    # #p2
    # intcode = parse(filename)
    # answer_b = run_program_2(intcode)
    # print(f"p2: {answer_b}")
    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    inp = "input.txt"

    sample_a_answer = 81
    # sample_b_answer = 18216

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
    answer_a, answer_b = main(inp)
    print(f"Your input answers: \nA: {answer_a}\nB: {answer_b}")
    try:
        submit_answer(answer_a, "a", day=15, year=2019)
    except AocdError:
        submit_answer(answer_b, "b", day=15, year=2019)
