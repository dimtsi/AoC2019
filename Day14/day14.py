from collections import Counter, defaultdict, deque
from functools import reduce, lru_cache
from itertools import permutations, combinations
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
from math import lcm

from intcode import IntCode
from math import ceil, floor

ORE_NEEDED = defaultdict(lambda: 0)
SURPLUSES = defaultdict(lambda: 0)

def parse(filename: str) -> IntCode:
    with open(filename, "r") as f:
        recipe = defaultdict(dict)

        lines = f.read().strip().split("\n")

    for line in lines:

        inp, out = line.split(" => ")
        in_elems = [x for x in re.findall("\w+", inp) if not x.isdigit()]
        in_n = [int(x) for x in re.findall("\w+", inp) if x.isdigit()]


        out_elem = [x for x in re.findall("\w+", out) if not x.isdigit()][0]
        out_n = [int(x) for x in re.findall("\w+", out) if x.isdigit()][0]
        if out_elem in recipe:  # multiple routes for creation
            assert False
        recipe[out_elem]['q'] = out_n
        recipe[out_elem]['ing'] = defaultdict(dict)
        for in_el, q in zip(in_elems, in_n):
            recipe[out_elem]["ing"][in_el] = q
    return recipe


def get_ingr(el, recipe):
    return recipe[el]['ing'].keys()


def quantity(el, recipe):
    return recipe[el]['q']


def get_ingr_q(el, recipe):
    return recipe[el]['ing'].items()


def find_quantity_to_make(elem, recipe, n_needed, surplus):
    total = 0
    if elem == "ORE":
        return n_needed

    # if elem in surplus:
    extra = min(n_needed, surplus[elem])
    n_needed -= extra
    surplus[elem] -= extra

    n_min = recipe[elem]['q']
    multiplier = ceil(n_needed / n_min)

    diff = multiplier * n_min - n_needed
    surplus[elem] += diff

    for ingr, q in get_ingr_q(elem, recipe):
        total += find_quantity_to_make(ingr, recipe, multiplier * q, surplus)

    return total

def get_max_fuel(recipe):
    stash = 1_000_000_000_000

    lower_bound, upper_bound = 1, 100

    while find_quantity_to_make(
            "FUEL", recipe, upper_bound, defaultdict(lambda: 0)) < stash:
        lower_bound = upper_bound
        upper_bound = upper_bound * 100


    print(f"searching_for_val_between: [{lower_bound}, {upper_bound}]")

    #binary search
    left, right = lower_bound, upper_bound

    while left + 1 < right:
        mid = (left + right) // 2

        mid_fuel = find_quantity_to_make("FUEL", recipe, mid, defaultdict(lambda: 0))

        if mid_fuel == stash:
            return mid
        elif mid_fuel > stash:
            right = mid
        elif mid_fuel < stash:
            left = mid
    return left


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    recipe = parse(filename)
    answer_a = find_quantity_to_make("FUEL", recipe, 1, defaultdict(lambda: 0))

    answer_b = get_max_fuel(recipe)
    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 2210736
    sample_b_answer = 460664

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
        submit_answer(answer_a, "a", day=14, year=2019)
    except AocdError:
        submit_answer(answer_b, "b", day=14, year=2019)
