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
from time import sleep

from intcode import IntCode


def parse(filename: str) -> IntCode:
    matrix = []
    with open(filename, "r") as f:
        lines = f.read().strip().replace("\n", "")

    l = [int(x) for x in lines.split(",")]

    d = {i: l[i] for i in range(len(l))}
    return IntCode(d)


def create_grid(seq):
    idx = 0
    pos_to_elem = defaultdict(lambda: 0)
    elem_positions = defaultdict(list)
    while idx < len(seq):
        y, x, id = seq[idx: idx + 3]
        # if not id in {3, 4}:
        pos_to_elem[(x, y)] = id
        elem_positions[id].append((x, y))
        idx += 3

    return pos_to_elem, elem_positions



def pprint(panel):
    min_x = min(panel, key=lambda x: x[0])[0]
    max_x = max(panel, key=lambda x: x[0])[0]
    min_y = min(panel, key=lambda x: x[1])[1]
    max_y = max(panel, key=lambda x: x[1])[1]

    range_x = max_x - min_x
    range_y = max_y - min_y

    output = [[" " for _ in range(range_y + 1)] for _ in range(range_x + 1)]

    for (x, y), id in panel.items():
        target_x = x - min_x
        target_y = y - min_y

        if id == 0:
            output[target_x][target_y] = "."
        elif id == 1:
            output[target_x][target_y] = "#"
        elif id == 2:
            output[target_x][target_y] = "B"
        elif id == 3:
            output[target_x][target_y] = "P"
        elif id == 4:
            output[target_x][target_y] = "o"

    for row in output:
        print("".join(row))
    print()




def run_program(intcode: IntCode, p2=False):

    intcode.run()
    outs = intcode.outs
    grid, elem_to_pos = create_grid(outs)

    pprint(grid)
    return len(elem_to_pos[2])


def run_program_2(intcode: IntCode):

    intcode.addr[0] = 2

    joystick_move = 0
    while not intcode.is_halted:
        intcode.inputs.extend([joystick_move])
        intcode.run()

        outs = intcode.outs
        grid, elem_to_pos = create_grid(outs)
        ball_pos = elem_to_pos[4]
        player_pos = elem_to_pos[3]

        (ball_y, ball_x) = ball_pos[-1]
        player_y, player_x = player_pos[-1]

        if player_x > ball_x:
            joystick_move = -1
        elif player_x < ball_x:
            joystick_move = 1
        else:
            joystick_move = 0
        # sleep(0.02)
        pprint(grid)
    return intcode.outs[-1]


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None
    intcode = parse(filename)
    answer_a = run_program(intcode)
    print(f"p1: {answer_a}")
    # #p2
    intcode = parse(filename)
    answer_b = run_program_2(intcode)
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
        submit_answer(answer_a, "a", day=13, year=2019)
    except AocdError:
        submit_answer(answer_b, "b", day=13, year=2019)
