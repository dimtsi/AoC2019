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


def parse(filename: str):
    matrix = []
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")
    all_keys = {}
    all_doors = {}
    start = None
    for i, line in enumerate(lines):
        for j in range(len(line)):
            if line[j].islower():
                all_keys[line[j]] = (i, j)
            elif line[j].isupper():
                all_doors[line[j]] = (i, j)
            elif line[j] == "@":
                start = (i, j)

    return [list(line) for line in lines], start, all_keys, all_doors


def pprint(grid):
    for row in grid:
        print("".join(row))


def get_neighbors_vals(
    matrix: List[List[str]],
    pos,
    found,
    all_doors=False,
) -> Generator[Tuple[Tuple[int, int], str], None, None]:

    i, j = pos

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

    if not all_doors:
        yield from (
            ((x, y), matrix[x][y])
            for (x, y) in neighbors
            if not (
                matrix[x][y] == "#"
                or (
                    matrix[x][y].isupper()
                    and matrix[x][y].lower() not in found
                )
            )
        )
    else:
        yield from (
            ((x, y), matrix[x][y])
            for (x, y) in neighbors
            if not (matrix[x][y] == "#")
        )


def dfs(pos, grid, start, visited, found, dist, p2=False):
    val = grid[pos[0]][pos[1]]

    if pos in visited and visited[pos] < dist:
        return
    visited[pos] = dist
    if val != "." and val != start:
        found[start][val] = dist
        if len(found) > 0:
            return

    neighbors = get_neighbors_vals(grid, pos, set(), all_doors=True, p2=p2)
    for neigh, val in neighbors:
        if neigh not in visited or visited[neigh] > dist + 1:
            dfs(neigh, grid, start, visited, found, dist + 1)

    return found


def create_adj_list(matrix, start_pos, all_keys, all_doors, p2=False):
    if not p2:
        all_elems = {"@": start_pos, **all_keys, **all_doors}
    else:
        all_elems = {**all_keys, **all_doors}
        all_elems.update(start_pos)

    adj = {}
    for elem in all_elems:
        adj.update(
            dfs(all_elems[elem], matrix, elem, dict(), defaultdict(dict), 0)
        )
    return adj


def min_cost(matrix, start_pos, all_keys, all_doors):
    G = create_adj_list(matrix, start_pos, all_keys, all_doors)
    complete = set()
    min_dist = float("inf")

    distances = defaultdict(lambda: float("inf"))
    start_state = ("@", tuple())
    distances[start_state] = 0
    pq = [(0, start_state)]
    visited = set()

    while pq:
        dist, state = heappop(pq)
        elem, found = state
        if state in visited:
            continue
        visited.add(state)

        neighbors = G[elem]
        if neighbors:
            for new_key, dist_to_key in neighbors.items():
                if new_key.isupper() and new_key.lower() not in found:
                    continue
                new_state = (
                    new_key,
                    found
                    if not new_key.islower()
                    else tuple(sorted(set(found) | set(new_key))),
                )

                if (
                    new_state not in visited
                    or distances[new_state] >= dist + dist_to_key
                ):
                    distances[new_state] = dist + dist_to_key
                    if len(new_state[1]) == len(all_keys):
                        complete.add(distances[new_state])
                        min_dist = min(min_dist, distances[new_state])
                        continue
                    heappush(pq, (dist + dist_to_key, new_state))

    return min_dist


def modify_grid_for_p2(grid, start):
    i, j = start

    grid[i + 1][j - 1] = "@1"
    grid[i + 1][j + 1] = "@2"
    grid[i - 1][j - 1] = "@3"
    grid[i - 1][j + 1] = "@4"

    grid[i][j + 1] = "#"
    grid[i + 1][j] = "#"
    grid[i - 1][j] = "#"
    grid[i][j - 1] = "#"
    grid[i][j] = "#"
    pprint(grid)
    start_positions = {
        "@1": (i + 1, j - 1),
        "@2": (i + 1, j + 1),
        "@3": (i - 1, j - 1),
        "@4": (i - 1, j + 1),
    }
    return start_positions


def get_keys_per_region(start, adj):
    visited = set()
    q = [start]
    region_keys = set()

    while q:
        elem = q.pop()
        if elem.islower():
            region_keys.add(elem)

        visited.add(elem)
        for neigh in adj[elem].keys():
            if neigh not in visited:
                q.append(neigh)
    return region_keys


def min_cost_p2(matrix, start_pos, all_keys, all_doors):
    G = create_adj_list(matrix, start_pos, all_keys, all_doors, p2=True)
    keys_per_region = [
        get_keys_per_region(x, G) for x in ("@1", "@2", "@3", "@4")
    ]

    complete = set()
    min_dist = float("inf")

    distances = defaultdict(lambda: float("inf"))
    start_state = (("@1", "@2", "@3", "@4"), tuple())
    distances[start_state] = 0
    pq = [(0, start_state)]
    visited = set()

    while pq:
        dist, state = heappop(pq)
        elements, found = state
        if state in visited:
            continue
        visited.add(state)

        for i, elem in enumerate(elements):
            if not set(keys_per_region[i]) - set(
                found
            ):  # already found all keys for specific one
                continue
            neighbors = G[elem]
            if neighbors:
                for new_key, dist_to_key in neighbors.items():
                    if new_key.isupper() and new_key.lower() not in found:
                        continue
                    new_state = (
                        tuple(
                            elements[j] if j != i else new_key
                            for j in range(4)
                        ),
                        found
                        if not new_key.islower()
                        else tuple(sorted(set(found) | set(new_key))),
                    )

                    if (
                        new_state not in visited
                        or distances[new_state] > dist + dist_to_key
                    ):
                        distances[new_state] = dist + dist_to_key
                        if len(new_state[1]) == len(all_keys):
                            complete.add(distances[new_state])
                            min_dist = min(min_dist, distances[new_state])
                            continue
                        heappush(pq, (dist + dist_to_key, new_state))

    return min_dist


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None
    grid, start_pos, all_keys, all_doors = parse(filename)
    answer_a = min_cost(grid, start_pos, all_keys, all_doors)
    print(f"p1: {answer_a}")
    # p2
    if "sample" in filename:
        filename = "sample2.txt"
    grid, start_pos, all_keys, all_doors = parse(filename)
    new_start_pos = modify_grid_for_p2(grid, start_pos)
    print()
    answer_b = min_cost_p2(grid, new_start_pos, all_keys, all_doors)
    print(f"p2: {answer_b}")
    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError
    from aocd.models import Puzzle

    puzzle = Puzzle(year=2019, day=18)

    sample = "sample.txt"
    inp = "input.txt"

    sample_a_answer = 132
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
    # try:
    #     submit_answer(answer_a, "a", day=15, year=2019)
    # except AocdError:
    #     submit_answer(answer_b, "b", day=15, year=2019)
