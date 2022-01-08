from collections import Counter, defaultdict, deque
from functools import reduce, lru_cache
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
from termcolor import colored
from copy import deepcopy
from heapq import heappop, heappush


def parse(filename: str):
    matrix = []
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")
    for line in lines:
        matrix.append(list(map(int, list(line))))
    return matrix


def get_neighbors_vals(
    matrix: List[List[Union[int, float]]], i: int, j: int
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

    yield from (((x, y), matrix[x][y]) for (x, y) in neighbors)


def min_cost(matrix):

    n_rows = len(matrix)
    n_cols = len(matrix[0])
    distances = defaultdict(lambda: float("inf"))
    origin = {}
    distances[(0, 0)] = 0
    pq = [(0, (0, 0))]
    visited = set()

    while pq:
        dist, elem = heappop(pq)
        if elem in visited:
            continue
        visited.add(elem)
        for (i, j), val in get_neighbors_vals(matrix, *elem):
            if (i, j) not in visited and distances[(i, j)] > dist + val:
                distances[(i, j)] = dist + val
                origin[(i, j)] = elem
                heappush(pq, (dist + val, (i, j)))

    return distances[(n_rows - 1, n_cols - 1)], origin


def construct_new_array(matrix):
    n_rows_old, n_cols_old = len(matrix), len(matrix[0])
    new_matrix = [
        [0 for _ in range(n_rows_old * 5)] for _ in range(n_cols_old * 5)
    ]
    n_rows_new, n_cols_new = len(new_matrix), len(new_matrix[0])

    for i in range(n_rows_new):
        for j in range(n_cols_new):
            di = i // n_rows_old
            dj = j // n_cols_old
            new_matrix[i][j] = matrix[i % n_rows_old][j % n_cols_old] + di + dj
            if new_matrix[i][j] >= 10:
                new_matrix[i][j] %= 9
    return new_matrix


def print_path(matrix, origin):
    num_rows = len(matrix)
    num_cols = len(matrix[0])

    path = set()
    node = (num_rows - 1, num_cols - 1)
    while node != (0, 0):
        next_node = origin[node]
        path.add(node)
        node = next_node
    for i in range(num_rows):
        row_str = ""
        for j in range(num_cols):
            val = matrix[i][j]
            if (i, j) in path:
                row_str += colored(str(val), "green")
            else:
                row_str += f"{str(val)}"
        print(row_str)


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    matrix = parse(filename)
    answer_a, origin1 = min_cost(matrix)
    print_path(matrix, origin1)
    new_array = construct_new_array(matrix)
    answer_b, origin2 = min_cost(new_array)
    print_path(new_array, origin2)

    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 40
    sample_b_answer = 315

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
    answer_a, answer_b = main(input)
    print(f"Your input answers: \nA: {answer_a}\nB: {answer_b}")
    try:
        submit_answer(answer_a, "a")
    except AocdError:
        submit_answer(answer_b, "b")
