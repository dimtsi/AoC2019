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

from intcode import IntCode


def parse(filename: str) -> Dict:
    matrix = []
    with open(filename, "r") as f:
        lines = f.read().strip().replace("\n", "")

    l = [int(x) for x in lines.split(",")]

    d = {i: l[i] for i in range(len(l))}
    return IntCode(d)





def run_program(intcode: IntCode, inp: List):
    intcode.inputs.extend(inp)
    intcode.run()
    return intcode.outs[-1]


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None
    intcode = parse(filename)
    answer_a = run_program(intcode, [1])
    print(f"p1: {answer_a}")
    # #p2
    # if "sample" in filename:
    #     filename = "sample2.txt"
    intcode = parse(filename)
    answer_b = run_program(intcode, [2])
    print(f"p2: {answer_b}")
    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

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
    answer_a, answer_b = main(input)
    # print(f"Your input answers: \nA: {answer_a}\nB: {answer_b}")
    # try:
    #     submit_answer(answer_a, "a", day=7, year=2019)
    # except AocdError:
    #     submit_answer(answer_b, "b", day=7, year=2019)
