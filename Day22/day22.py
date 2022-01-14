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
        lines = f.read().strip().split("\n")

    cmds = []

    for line in lines:
        if "deal into" in line:
            cmds.append(("stack", 0))
        else:
            num = int(re.findall("-?\d+", line)[0])
            if "cut" in line:
                cmds.append(("cut", num))

            elif "increment" in line:
                cmds.append(("inc", num))
    return cmds


def cut(curr_pos, n_cut, size):
    if n_cut > 0:
        if curr_pos >= n_cut:
            new_pos = curr_pos - n_cut
        else:
            new_pos = size + curr_pos - n_cut
    else:
        return cut(curr_pos, size - abs(n_cut), size)
    return new_pos


def incr(curr_pos, inc, size):
    out = (curr_pos * inc) % size
    return out


def get_new_position(cmd_val, curr_pos, size):
    cmd, val = cmd_val
    if cmd == "stack":
        return (size - curr_pos - 1) % size
    elif cmd == "cut":
        return (curr_pos - val) % size
    elif cmd == "inc":
        return (curr_pos * val) % size



def run(cmds, target_num, size):
    pos = target_num
    for cmd in cmds:
        pos = get_new_position(cmd, pos, size)

    return pos


def run_p2(cmds, target_num, size, n_steps):
    start_pos = target_num
    new_pos, prev_pos = start_pos, start_pos
    count = 0
    for i in range(n_steps):
        if new_pos == start_pos and i != 0:
            break
        new_pos = run(cmds, new_pos, size)
        print(new_pos - prev_pos)
    print()




#
# def get_full_list(cmds, size):
#     final = [None for _ in range(size)]
#     try:
#         for i in range(size):
#             new_pos = run(cmds, i, size)
#             final[new_pos] = i
#     except:
#         pass
#     print()




def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None
    cmds = parse(filename)
    if "sample" in filename:
        answer_a = run(cmds, 7, 10)
    else:
        answer_a = run(cmds, 2019, 10007)
    # answer_a = get_full_list(cmds, 10)
    print(f"p1: {answer_a}")
    # p2
    if not "sample" in filename:
        answer_b = run_p2(cmds, 2020, 119315717514047, 101741582076661)
    print(f"p2: {answer_b}")
    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":
    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    inp = "input.txt"

    sample_a_answer = 6
    sample_b_answer = 18216

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
    # try:
    #     submit_answer(answer_a, "a", day=15, year=2019)
    # except AocdError:
    #     submit_answer(answer_b, "b", day=15, year=2019)
