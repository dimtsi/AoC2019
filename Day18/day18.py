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


def pprint(grid):
    for row in grid:
        print("".join(row))


def get_neighbors_vals(
    matrix: List[List[str]], state: State,
    p2=False) -> Generator[Tuple[Tuple[int, int], str], None, None]:
    if not p2:
        (i, j), found = state
    else:
        curr_positions, found, move = state
        i, j = curr_positions[move]

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
        dist, state = heappop(pq)
        if state in visited or dist > min_dist:
            continue
        visited.add(state)
        for (i, j), val in get_neighbors_vals(matrix, state):

            new_state = ((i, j), state[1])

            if val.islower():
                new_pos, new_found = new_state
                new_state = ((i, j), tuple(sorted(set(new_found) | set(val))))
            if new_state not in visited or distances[new_state] > dist + 1:
                if dist + 1 > min_dist:
                    continue
                distances[new_state] = dist + 1
                if val.islower() and len(new_state[1]) == len(all_keys):
                    complete_pos_dist.add((new_state, distances[new_state]))
                    complete.add(distances[new_state])
                    min_dist = min(complete)
                    continue
                heappush(pq, (dist + 1, new_state))
    min_dist = min(complete)

    return min_dist


def modify_grid_for_p2(grid, start):
    i, j = start

    grid[i + 1][j - 1] = "@"
    grid[i + 1][j + 1] = "@"
    grid[i - 1][j - 1] = "@"
    grid[i - 1][j + 1] = "@"

    grid[i][j + 1] = "#"
    grid[i + 1][j] = "#"
    grid[i - 1][j] = "#"
    grid[i][j - 1] = "#"
    grid[i][j] = "#"
    pprint(grid)
    start_positions = (
        (i + 1, j - 1),
        (i + 1, j + 1),
        (i - 1, j - 1),
        (i - 1, j + 1),
    )
    return start_positions


def get_new_states(state, new_pos, val):
    move = state[2]
    new_state = [list(state[0]), state[1], state[2]]
    new_state[0][move] = new_pos
    if val.islower():
        new_state[1] = tuple(sorted(set(new_state[1]) | set(val)))
    for i in range(4):
        yield tuple([tuple(new_state[0]), new_state[1], i])



def min_cost_p2(matrix, start, all_keys):

    complete = set()
    complete_pos_dist = set()
    min_dist = float("inf")
    start_states = list((start, tuple(), i) for i in range(4))

    distances = defaultdict(lambda: float("inf"))
    distances.update({state: 0 for state in start_states})
    pq = [(0, state) for state in start_states]
    visited = set()

    while pq:
        dist, state = heappop(pq)
        if state in visited or dist > min_dist:
            continue
        visited.add(state)
        for (i, j), val in get_neighbors_vals(matrix, state, p2=True):
            new_states = list(get_new_states(state, (i, j), val))
            # new_state = ((i, j), state[1])

            for new_state in new_states:

                # new_pos, new_found, new_move = new_state
                # if new_found == ("b", "c") and new_move == 2:
                #     x = new_state in visited
                #     y = distances[new_state]
                #     print()

                if new_state not in visited or distances[new_state] > dist + 1:
                    # if dist + 1 > min_dist:
                    #     continue
                    distances[new_state] = dist + 1
                    if val.islower() and len(new_state[1]) == len(all_keys):
                        complete_pos_dist.add((new_state, distances[new_state]))
                        complete.add(distances[new_state])
                        min_dist = min(complete)
                        continue
                    heappush(pq, (dist + 1, new_state))
    min_dist = min(complete)

    return min_dist


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None
    grid, start_pos, all_keys = parse(filename)
    answer_a = min_cost(grid, start_pos, all_keys)
    print(f"p1: {answer_a}")
    # #p2
    grid, start_pos, all_keys = parse(filename)
    new_start_pos = modify_grid_for_p2(grid, start_pos)
    pprint(grid)
    answer_b = min_cost_p2(grid, new_start_pos, all_keys)
    # print(f"p2: {answer_b}")
    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    inp = "input.txt"

    sample_a_answer = 114
    sample_b_answer = 72

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
