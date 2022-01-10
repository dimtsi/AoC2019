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


def pprint(grid, path=False):
    G = deepcopy(grid)
    if path:
        G = [list(row) for row in G]
        for (x, y), curr_dir in path:
            G[x][y] = curr_dir

    for row in G:
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
    matrix = "".join(grid_s).strip().split("\n\n")[0].split("\n")
    print(f"Matrix:\n{''.join(grid_s)}")
    return matrix





def find_start_intersections(matrix):
    intersections = []
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == "#":
                neighbors = list(get_neighbors_vals(matrix, i, j, walls_only=True))
                if len(list(get_neighbors_vals(matrix, i, j, walls_only=True))) == 4:
                    intersections.append((i, j))
            elif matrix[i][j] in {"^", "<", ">", "v"}:
                start = ((i, j), matrix[i][j])

    return start, intersections

def str_to_cmd(string):
    cmd = [ord(i) for i in string]
    return cmd


def print_out(intcode):
    outs = [chr(char) for char in intcode.outs]
    for grid in "".join(outs).split("\n\n"):
        print(grid)
        from time import sleep
        sleep(1)



def turn(pos, target_pos, curr_dir):
    
    curr_x, curr_y = pos
    target_x, target_y = target_pos
    
    dx = target_x - curr_x
    dy = target_y - curr_y
    
    if curr_dir == "^":
        return ("L", "<") if dy < 0 else ("R", ">")
        
    elif curr_dir == "<":
        return ("L", "v") if dx > 0 else ("R", "^")
    
    elif curr_dir == ">":
        return ("L", "^") if dx < 0 else ("R", "v")
    
    elif curr_dir == "v":
        return ("L", ">") if dy > 0 else ("R", "<")
    
    
def next_forward(grid, i, j, curr_dir) -> Optional[Tuple]:
    num_rows = len(grid)
    num_cols = len(grid[i])

    if i - 1 >= 0 and curr_dir == "^" and grid[i-1][j] == "#":
        return (i - 1, j)
    elif i + 1 < num_rows and curr_dir == "v" and grid[i+1][j] == "#":
        return (i + 1, j)
    elif j - 1 >= 0 and curr_dir == "<" and grid[i][j - 1] == "#":
        return (i, j - 1)
    elif j + 1 < num_cols and curr_dir == ">" and grid[i][j + 1] == "#":
        return (i, j + 1)


def create_path(grid, start_pos, start_dir):
    
    q = [(start_pos, start_dir)]
    path = []
    path_cmd = []
    set_path = set()
    while q:
        pos, curr_dir = q.pop()
        path.append((pos, curr_dir))
        set_path.add(pos)
        steps = 1
        while next_forward(grid, *pos, curr_dir):
            steps += 1
            pos = next_forward(grid, *pos, curr_dir)
            path.append((pos, curr_dir))
            set_path.add(pos)
        #turn
        if steps > 1:
            path_cmd.append(str(steps))
        # pos = path[-2]
        neighbors = get_neighbors_vals(grid, *pos, walls_only=True)
        for neigh, _ in neighbors:
            if neigh not in set_path:
                new_turn, new_dir = turn(pos, neigh, curr_dir)
                path_cmd.append(new_turn)
                q.append((neigh, new_dir))
    print(",".join([str(x) for x in path_cmd]))
    return path


def get_grid_and_intersections(intcode):

    grid: List[List[str]] = create_grid(intcode)
    start, intersections = find_start_intersections(grid)
    return grid, start, intersections


def create_sequence():
    final = "A,B,A,C,B,C,A,B,A,C\n"
    A = "R,8,R,8\n"
    B = "L,5,L,5\n"
    C = "R,5,R,3\n"
    A = "R,6,L,10,R,8,R,8\n"
    B = "R,12,L,8,L,10\n"
    C = "R,12,L,10,R,6,L,10\n"

    final += A + B + C + "n\n"
    return final

def run_program_2(intcode):
    intcode.addr[0] = 2
    grid, start, intersections = get_grid_and_intersections(intcode)

    path = create_path(grid, start[0], start[1])
    pprint(grid, path=path)


    intcode.inputs.extend(str_to_cmd(create_sequence()))
    intcode.run()

    return intcode.outs[-1]


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None
    intcode = parse(filename)
    grid, start_pos, intersections = get_grid_and_intersections(intcode)
    answer_a = sum([x * y for x, y in intersections])
    print(f"p1: {answer_a}")
    #p2
    intcode = parse(filename)
    answer_b = run_program_2(intcode)
    print(f"p2: {answer_b}")
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
