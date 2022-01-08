from collections import Counter, defaultdict, deque
from functools import reduce, lru_cache
from itertools import product
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


def parse(filename: str) -> List:
    with open(filename, "r") as f:
        wires_raw = [wire.split(",") for wire in f.read().strip().split("\n")]

    wire_coords = [[], []]
    for i, wire in enumerate(wires_raw):
        start = (0, 0)
        for move in wire:
            d, x = move[0], int(move[1:])
            if d == "U":
                end = start[0] + x, start[1]
            elif d == "D":
                end = start[0] - x, start[1]
            elif d == "L":
                end = start[0], start[1] - x
            elif d == "R":
                end = start[0], start[1] + x
            wire_coords[i].append(tuple([start, end]))
            start = end

    return wire_coords


def get_min_maxes(line):
    x_min = min(line, key=lambda x: x[0])[0]
    x_max = max(line, key=lambda x: x[0])[0]
    y_min = min(line, key=lambda x: x[1])[1]
    y_max = max(line, key=lambda x: x[1])[1]
    return x_min, x_max, y_min, y_max


def find_intersection(line1, line2):
    line1_start, line1_end = line1
    line2_start, line2_end = line2

    is_horizontal_1 = is_vertical_1 = is_horizontal_2 = is_vertical_2 = False

    if line1_start[0] - line1_end[0] == 0:
        is_vertical_1 = True
    if line2_start[0] - line2_end[0] == 0:
        is_vertical_2 = True
    if line1_start[1] - line1_end[1] == 0:
        is_horizontal_1 = True
    if line2_start[1] - line2_end[1] == 0:
        is_horizontal_2 = True
    #check if parallel
    if is_horizontal_1 and is_horizontal_2:
        return None
    elif is_vertical_1 and is_vertical_2:
        return None

    #check intersection possibility
    x_min_1, x_max_1, y_min_1, y_max_1 = get_min_maxes(line1)
    x_min_2, x_max_2, y_min_2, y_max_2 = get_min_maxes(line2)

    if x_min_1 > x_max_2 or x_max_1 < x_min_2 or y_min_1 > y_max_2 or y_max_1 < y_min_2:
        return None
    else:
        if not ((0, 0) in line1 and (0, 0) in line2):
            if is_horizontal_1:
                return x_min_2, y_min_1
            else:
                return x_min_1, y_min_2


def manhattan(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


def find_intersections(positions: List[List[Tuple]]):
    dists = {}

    dist1 = 0
    dist2 = 0

    min_manh = float("inf")
    pairs1, pairs2 = positions
    for i, pair1 in enumerate(pairs1):
        for j, pair2 in enumerate(pairs2):
            intersection = find_intersection(pair1, pair2)
            if intersection:
                min_manh = min(min_manh, manhattan((0, 0), intersection))
                if not intersection in dists:
                    dists[intersection] = sum([
                        dist1 + manhattan(pair1[0], intersection),
                        dist2 + manhattan(pair2[0], intersection)
                    ])
            dist2 += manhattan(*pair2)

        dist1 += manhattan(*pair1)
        dist2 = 0
    return min_manh, min(dists.values())


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    start = time()
    answer_a, answer_b = None, None

    init_positions = parse(filename)
    # ver_count, end_idx, val = parse_string(s, 0, 0)
    answer_a, answer_b = find_intersections(init_positions)
    # init_positions = parse(filename)
    # answer_b = find_gravity(init_positions)
    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample1.txt"
    input = "input.txt"

    sample_a_answer = 6
    sample_b_answer = 50346

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
    try:
        submit_answer(answer_a, "a", day=3, year=2019)
    except AocdError:
        submit_answer(answer_b, "b", day=3, year=2019)
