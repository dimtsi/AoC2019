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
    all_keys = {}
    for i, line in enumerate(lines):
        for j in range(len(line)):
            if line[j].islower():
                all_keys[line[j]] = (i, j)
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


def dfs(state, grid, visited: Dict, found, dist, p2=False):
    curr_pos = state[0] if not p2 else state[0][state[2]]
    val = grid[curr_pos[0]][curr_pos[1]]

    visited[state] = val

    neighbors = get_neighbors_vals(grid, state, p2)
    for neigh, val in neighbors:
        new_state = (neigh, state[1] if not val.islower() else tuple(sorted(set(state[1]) | set(val))))
        if (new_state) not in visited:
            if val.islower() and val not in state[1]:
                found[state][new_state] = dist + 1
                dfs(new_state, grid, visited, found, dist + 1)
            else:
                dfs((neigh, state[1]), grid, visited, found, dist + 1)
    return found


def min_cost(matrix, start, all_keys):

    complete = set()
    min_dist = float("inf")
    start_state = (start, tuple())

    distances = defaultdict(lambda: float("inf"))
    distances[start_state] = 0
    pq = [(0, start_state)]
    visited = set()

    # x = dfs(start_state, matrix, dict(), dict(), 0)
    # print()
    while pq:
        dist, state = heappop(pq)
        if state in visited or dist > min_dist:
            continue
        visited.add(state)
        candidates = dfs(state, matrix, dict(), defaultdict(dict), 0)
        if candidates:
            for new_key, dist_to_key in candidates.items():
                found_keys = tuple(sorted(set(state[1]) | set(new_key)))
                new_state = (all_keys[new_key], found_keys)

                if new_state not in visited and distances[new_state] > dist + dist_to_key:
                    distances[new_state] = dist + dist_to_key
                    if len(new_state[1]) == len(all_keys):
                        complete.add(distances[new_state])
                        min_dist = min(complete)
                        continue
                    heappush(pq, (dist + dist_to_key, new_state))
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
        for i in range(4):
            candidates = dfs((state[0], state[1], i), matrix, dict(), dict(), 0, p2=True)
            if candidates:
                for new_key, dist_to_key in candidates.items():
                    found_keys = tuple(sorted(set(state[1]) | set(new_key)))
                    new_positions = tuple(state[0][j] if j != i else all_keys[new_key] for j in range(4))
                    new_state = (new_positions, found_keys, 0)

                    if new_state not in visited and distances[
                        new_state] >= dist + dist_to_key:
                        distances[new_state] = dist + dist_to_key
                        if len(new_state[1]) == len(all_keys):
                            complete.add(distances[new_state])
                            min_dist = min(complete)
                            continue
                        heappush(pq, (dist + dist_to_key, new_state))
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
    if "sample" in filename:
        filename = "sample2.txt"
    grid, start_pos, all_keys = parse(filename)
    new_start_pos = modify_grid_for_p2(grid, start_pos)
    print()
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

    sample_a_answer = 136
    sample_b_answer = 72

    answer_a, answer_b = main(inp)
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
    # try:
    #     submit_answer(answer_a, "a", day=15, year=2019)
    # except AocdError:
    #     submit_answer(answer_b, "b", day=15, year=2019)
