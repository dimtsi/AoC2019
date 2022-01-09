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


def create_grid(grid, print_grid=False):
    min_x = min(grid, key=lambda x: x[0])[0]
    max_x = max(grid, key=lambda x: x[0])[0]
    min_y = min(grid, key=lambda x: x[1])[1]
    max_y = max(grid, key=lambda x: x[1])[1]

    range_x = max_x - min_x
    range_y = max_y - min_y

    output = [
        [float("inf") for _ in range(range_y + 1)] for _ in range(range_x + 1)
    ]

    for (x, y), id in grid.items():
        target_x = x - min_x
        target_y = y - min_y

        if (x, y) == (0, 0):
            source = target_x, target_y
            output[target_x][target_y] = 0
        elif id == 1:
            output[target_x][target_y] = 1
        elif id == 2:
            target = (target_x, target_y)
            output[target_x][target_y] = 2

    if print_grid:
        pprint(output, None)

    return output, source, target


def pprint(grid, oxygen):
    grid = deepcopy(grid)
    if oxygen:
        for i, j in oxygen:
            grid[i][j] = 3

    match = {float("inf"): "#", 0: "S", 1: ".", 2: "T", 3: "O"}
    for row in grid:
        new_row = [match[el] for el in row]
        print("".join(new_row))


def explore_neighbors(intcode):
    found = []
    for move in [1, 2, 3, 4]:
        intcode.add_input(move)
        intcode.run()
        found.append(intcode.outs[-1])
        # reverse to start
        if intcode.outs[-1] in {1, 2}:
            intcode.add_input(BACKTR[move])
            intcode.run()
    return found


def out_idx_to_coords(idx, pos):
    i, j = pos
    if idx == 0:
        return i - 1, j
    elif idx == 1:
        return i + 1, j
    elif idx == 2:
        return i, j - 1
    elif idx == 3:
        return i, j + 1


def dfs(curr: Tuple, move, intcode: IntCode, visited: Dict, walls: Set):
    curr_pos, val = curr
    assert curr_pos not in walls  #test
    if move:
        intcode.add_input(move)
        intcode.run()
    visited[curr_pos] = val
    neighbors = explore_neighbors(intcode)
    for i, neigh in enumerate(neighbors):
        neigh_pos = out_idx_to_coords(i, curr_pos)
        if neigh == 0:
            walls.add(neigh_pos)
        else:
            if neigh_pos in visited:
                assert neigh == visited[neigh_pos]  #test
            else:
                dfs((neigh_pos, neigh), i + 1, intcode, visited, walls)
    if move:
        intcode.add_input(BACKTR[move])
        intcode.run()

    return visited


def print_path(matrix, origin, start, end):
    num_rows = len(matrix)
    num_cols = len(matrix[0])

    path = set()
    node = end
    while node != start:
        next_node = origin[node]
        path.add(node)
        node = next_node
    path.add(start)

    match = {float("inf"): "#", 0: "S", 1: ".", 2: "T"}
    matrix[start[0]][start[1]] = 0
    matrix[end[0]][end[1]] = 2

    for i in range(num_rows):
        row_str = ""
        for j in range(num_cols):
            val = match[matrix[i][j]]
            if (i, j) in path:
                row_str += colored(str(val), "red")
            else:
                row_str += f"{str(val)}"
        print(row_str)


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

    yield from (
        ((x, y), matrix[x][y])
        for (x, y) in neighbors
        if not matrix[x][y] == float("inf")
    )


def min_cost(matrix, start, end):

    matrix[start[0]][start[1]] = 0
    matrix[end[0]][end[1]] = 1

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
        for (i, j), val in get_neighbors_vals(matrix, *elem):
            if (i, j) not in visited and distances[(i, j)] > dist + val:
                distances[(i, j)] = dist + val
                origin[(i, j)] = elem
                heappush(pq, (dist + val, (i, j)))

    return distances[end], origin


def steps_for_oxygen(grid, start):
    total_free = sum(row.count(1) + row.count(2) for row in grid)

    oxygen = {start}
    new_stack = [start]
    n_steps = 0

    while len(oxygen) < total_free:
        pprint(grid, oxygen)
        stack = new_stack[:]
        new_stack = []
        while stack:
            elem = stack.pop()
            for neigh, val in get_neighbors_vals(grid, *elem):
                if neigh not in oxygen:
                    new_stack.append(neigh)
        oxygen.update(new_stack)
        n_steps += 1

    return n_steps





def run_program(intcode: IntCode):
    empty_positions = dfs(((0, 0), 1), None, intcode, dict(), set())
    grid, source, target = create_grid(empty_positions, print_grid=True)
    min_dist, origin = min_cost(grid, source, target)
    print_path(grid, origin, source, target)
    #p2

    ox_steps = steps_for_oxygen(grid, target)
    return min_dist, ox_steps


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None
    intcode = parse(filename)
    answer_a, answer_b = run_program(intcode)
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
    try:
        submit_answer(answer_a, "a", day=15, year=2019)
    except AocdError:
        submit_answer(answer_b, "b", day=15, year=2019)
