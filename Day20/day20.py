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
        matrix = f.read().split("\n")

    max_len = 0
    for i, line in enumerate(matrix):
        matrix[i] = list(line)
        max_len = max(max_len, len(line))

    # fill in trailing spaces
    for row in matrix:
        [row.append(" ") for _ in range(len(row), max_len)]

    portals = get_portals(matrix)

    return matrix, portals


def get_portals(matrix):
    portal_pos = defaultdict(list)
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            val = matrix[i][j]
            if j + 1 < len(matrix[0]):
                if matrix[i][j].isupper() and matrix[i][j + 1].isupper():
                    if j + 2 == len(matrix[0]):
                        portal_pos[val + matrix[i][j + 1]].append(
                            ((i, j - 1), "outer")
                        )
                    elif matrix[i][j + 2] == " ":
                        portal_pos[val + matrix[i][j + 1]].append(
                            ((i, j - 1), "inner")
                        )
                    elif j == 0:
                        portal_pos[val + matrix[i][j + 1]].append(
                            ((i, j + 2), "outer")
                        )
                    else:
                        portal_pos[val + matrix[i][j + 1]].append(
                            ((i, j + 2), "inner")
                        )
            if i + 1 < len(matrix):
                if matrix[i][j].isupper() and matrix[i + 1][j].isupper():
                    if i + 2 == len(matrix):
                        portal_pos[val + matrix[i + 1][j]].append(
                            ((i - 1, j), "outer")
                        )
                    elif matrix[i + 2][j] == " ":
                        portal_pos[val + matrix[i + 1][j]].append(
                            ((i - 1, j), "inner")
                        )
                    elif i == 0:
                        portal_pos[val + matrix[i + 1][j]].append(
                            ((i + 2, j), "outer")
                        )
                    else:
                        portal_pos[val + matrix[i + 1][j]].append(
                            ((i + 2, j), "inner")
                        )
    portals = {}

    for key, positions in portal_pos.items():
        if key == "AA":
            portals["start"] = (positions[0][0], "inner")
        elif key == "ZZ":
            portals["end"] = (positions[0][0], "outer")
        else:
            pos1, pos2 = positions[0][0], positions[1][0]
            portals[pos1] = pos2, positions[0][1]
            portals[pos2] = pos1, positions[1][1]
    return portals


def pprint(grid):
    for row in grid:
        print("".join(row))


def get_neighbors_vals(
    matrix: List[List[str]], i: int, j: int, portals: Dict
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

    if (i, j) in portals:
        neighbors.append(portals[(i, j)][0])

    yield from (
        ((x, y), matrix[x][y]) for (x, y) in neighbors if matrix[x][y] == "."
    )


def min_cost(matrix, portals):

    start = portals["start"][0]
    end = portals["end"][0]

    distances = defaultdict(lambda: float("inf"))
    origin = {}
    distances[start] = 0
    pq = [(0, start)]
    visited = set()

    while pq:
        dist, elem = heappop(pq)
        if elem in visited:
            continue
        visited.add(elem)
        for (i, j), _ in get_neighbors_vals(matrix, *elem, portals):
            if (i, j) not in visited and distances[(i, j)] > dist + 1:
                distances[(i, j)] = dist + 1
                origin[(i, j)] = elem
                heappush(pq, (dist + 1, (i, j)))

    return distances[end], origin


def get_neighbors_p2(
    matrix: List[List[str]],
    i: int,
    j: int,
    portals: Dict,
    depth: int,
    start_pos,
    end_pos,
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

    if (i, j) in portals:
        if (i, j) == end_pos:
            if depth != 0:
                yield (i, j), 0
        elif (i, j) == start_pos:
            if depth == 0:
                yield (i, j), 1
        else:
            new_pos, in_out = portals[(i, j)]
            if in_out == "inner":
                yield new_pos, depth + 1
            else:
                if depth - 1 >= 0:
                    yield new_pos, depth - 1

    yield from (((x, y), depth) for (x, y) in neighbors if matrix[x][y] == ".")


def min_cost_p2(matrix, portals):

    start_pos = portals["start"][0]
    end_pos = portals["end"][0]

    distances = defaultdict(lambda: float("inf"))
    origin = {}
    distances[(start_pos, 0)] = 0
    pq = [(0, (start_pos, 0))]
    visited = set()

    while pq:
        dist, (elem, depth) = heappop(pq)
        if (elem, depth) in visited:
            continue

        visited.add((elem, depth))
        for (i, j), new_depth in get_neighbors_p2(
            matrix, *elem, portals, depth, start_pos, end_pos
        ):
            if not new_depth > len(portals) and ((i, j), new_depth) not in visited and distances[
                ((i, j), new_depth)
            ] > dist + 1:
                distances[((i, j), new_depth)] = dist + 1
                # origin[(i, j)] = elem
                heappush(pq, (dist + 1, ((i, j), new_depth)))
    min_dist = distances[(end_pos, 0)]
    return distances[(end_pos, 0)], origin


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None
    grid, portals = parse(filename)
    answer_a, path = min_cost(grid, portals)
    print(f"p1: {answer_a}")
    # #p2
    if "sample" in filename:
        filename = "sample2.txt"
    grid, portals = parse(filename)
    answer_b, path = min_cost_p2(grid, portals)
    print(f"p2: {answer_b}")
    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    inp = "input.txt"

    sample_a_answer = 23
    sample_b_answer = 396

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
        submit_answer(answer_a, "a", day=20, year=2019)
    except AocdError:
        submit_answer(answer_b, "b", day=20, year=2019)
