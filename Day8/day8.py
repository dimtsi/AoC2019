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
from copy import deepcopy
import re

PATHS_TO_END = []

def parse(filename: str) -> List:

    with open(filename, "r") as f:
        inp = [int(x) for x in list(f.read().strip())]

    return inp


def get_layers(digits, shape):
    n_layer = shape[0] * shape[1]
    layers = []

    idx = 0
    while idx < len(digits):
        layers.append(digits[idx: idx + n_layer])
        idx += n_layer
    return layers

def p1(digits, shape):
    layers = get_layers(digits, shape)

    fewest_zero_layer = sorted(layers, key=lambda x: Counter(x)[0])[0]
    counter = Counter(fewest_zero_layer)
    return counter[1] * counter[2]


def pprint(arr, shape):
    out_im = [[None for _ in range(shape[1])] for _ in range(shape[0])]

    for i in range(len(arr)):
        x = i // shape[1]
        y = i % shape[1]

        out_im[x][y] = " " if arr[i] == 0 else "#"

    import numpy as np
    x = np.array(out_im)
    for row in out_im:
        print("".join(row))



def p2(digits, shape):
    layers = get_layers(digits, shape)
    final_image = [None for i in range(len(layers[0]))]
    for i in range(len(layers[0])):
        layer_idx = 0
        while True:
            val = layers[layer_idx][i]
            if val != 2:
                final_image[i] = val
                break
            else:
                layer_idx += 1
    pprint(final_image, shape)
    return final_image




def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time
    start = time()

    answer_a, answer_b = None, None
    digits = parse(filename)
    shape = (3, 2) if "sample" in filename else (6, 25)
    answer_a = p1(digits, shape)
    # #p2
    if "sample" in filename:
        filename = "sample2.txt"
    digits = parse(filename)
    shape = (2, 2) if "sample" in filename else (6, 25)
    answer_b = p2(digits, shape)
    # run_program(intcode, inp=5)
    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 1
    # sample_b_answer = 4

    answer_a, answer_b = main(sample)
    assert (
        answer_a == sample_a_answer
    ), f"AnswerA incorrect: Actual: {answer_a}, Expected: {sample_a_answer}"
    print("sampleA correct")
    # if answer_b:
    #     assert (
    #         answer_b == sample_b_answer
    #     ), f"AnswerB incorrect: Actual: {answer_b}, Expected: {sample_b_answer}"
    #     print("sampleB correct")


    # Test on your input and submit
    answer_a, answer_b = main(input)
    print(f"Your input answers: \nA: {answer_a}\nB: {answer_b}")
    # try:
    #     submit_answer(answer_a, "a", day=8, year=2019)
    # except AocdError:
    #     submit_answer(answer_b, "b", day=8, year=2019)

