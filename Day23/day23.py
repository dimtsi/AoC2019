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


def dispatch(outs, computers, NAT, p2):
    assert len(outs) % 3 == 0
    for i in range(0, len(outs), 3):
        addr, x, y = outs[i], outs[i+1], outs[i+2]
        if addr == 255:
            if not p2:
                print(addr, x, y)
                return addr, x, y, None
            else:
                NAT = [x, y]
                continue

        computers[addr].inputs.extend([x, y])
    return None, None, None, NAT


def check_idle(comps):

    for comp in comps:
        if comp.inputs:
            return False
        elif comp.outs:
            return False
        elif not comp.waiting_for_input:
            return False
    return True


def run_program(intcode, p2=False):
    idle_cycle = 0
    NAT = []
    nat_history = []
    comps = [deepcopy(intcode) for _ in range(50)]
    [comp.inputs.extend([i]) for i, comp in enumerate(comps)]  # add address

    while True:
        for i in range(50):
            if not comps[i].inputs:
                comps[i].inputs = [-1]

            comps[i].run()
            outs = comps[i].outs[:]

            if outs:
                addr, x, y, NAT = dispatch(outs, comps, NAT, p2)
                if addr == 255 and not p2:
                    return y

        if p2:
            is_idle = check_idle(comps)
            idle_cycle += 1 if is_idle else 0
            if idle_cycle > 2 and is_idle:
                assert NAT, f"NAT empty"
                if nat_history and (NAT[-1] == nat_history[-1]):
                    return NAT[-1]
                comps[0].inputs.extend(NAT)
                nat_history.append(NAT[-1])
        [comp.flush_output() for comp in comps]



def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None
    intcode = parse(filename)
    answer_a = run_program(intcode)
    print(f"p1: {answer_a}")
    # p2
    intcode = parse(filename)
    answer_b = run_program(intcode, p2=True)
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
