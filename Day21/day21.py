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


def parse(filename: str) -> IntCode:
    matrix = []
    with open(filename, "r") as f:
        lines = f.read().strip().replace("\n", "")

    l = [int(x) for x in lines.split(",")]

    d = {i: l[i] for i in range(len(l))}
    return IntCode(d)


def str_to_cmd(string):
    cmd = [ord(i) for i in string]
    return cmd


def print_out(intcode):
    outs = [chr(char) for char in intcode.outs]
    for grid in "".join(outs).split("\n\n"):
        print(grid)
        from time import sleep
        sleep(0.3)
    # NOT B T
    # OR T J
    # NOT C T
    # OR J T
    # NOT D J
    # OR T J
    # WALK

def run_program(intcode):
    # cmd = "NOT A J\nNOT B J\nNOT C J\nNOT D J\nWALK\n"
    instr = """NOT C T
    NOT D J
    NOT J J
    AND T J
    NOT A T
    OR T J
    WALK
    """
    cmd = instr
    intcode.inputs.extend(str_to_cmd(cmd))
    intcode.run()
    try:
        print_out(intcode)
    except ValueError:
        return intcode.outs[-1]


def run_program_p2(intcode):
    instr = """NOT C J
    AND D J
    AND H J
    NOT B T
    AND D T
    OR T J
    NOT A T
    OR T J
    RUN
    """
    cmd = instr
    intcode.inputs.extend(str_to_cmd(cmd))
    intcode.run()
    try:
        print_out(intcode)
    except ValueError:
        return intcode.outs[-1]

def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None
    intcode = parse(filename)
    answer_a = run_program(intcode)
    print(f"p1: {answer_a}")
    # p2
    intcode = parse(filename)
    answer_b = run_program_p2(intcode)
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
