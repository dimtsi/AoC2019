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

from math import atan, degrees

def parse(filename: str) -> List:
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")

    grid = []
    for line in lines:
        grid.append(list(line))
    return grid


def pprint(arr, shape):
    for row in arr:
        print("".join(row))


def get_quadrant(x, y):
    if x > 0 and y > 0:
        return 1
    if x < 0 and y > 0:
        return 2
    if x < 0 and y < 0:
        return 3
    if x > 0 and y < 0:
        return 4


def get_angle(start: Tuple, end: Tuple):
    y, x = -(end[0] - start[0]), end[1] - start[1]

    if x == 0:
        if y > 0:
            val = float("inf")
        else:
            val = float("-inf")
    else:
        val = y / x

    degs = degrees(atan(val))
    quadr = get_quadrant(x, y)


    if quadr == 1:
        out = degs
    if quadr == 2:
        out = 180 - abs(degs)
    elif quadr == 3:
        out = 270 - abs(degs)
    elif quadr == 4:
        out = 360 - abs(degs)

    return out


def find_visible(x, y, grid):

    angle_vis = defaultdict(lambda: 0)
    angles = defaultdict(list)
    all_angles = defaultdict(list)

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if i == x and j == y:
                continue
            val = grid[i][j]
            if val != "#":
                continue
            if (y - j) != 0 and (x - i) != 0:
                ang = get_angle((x, y), (i, j))
                if ang in angles:
                    all_angles[ang].append((i, j))
                    continue

                angle_vis[ang] += 1
                angles[ang].append((i, j))
                all_angles[ang].append((i, j))
    # up
    for i in range(x - 1, -1, -1):
        if grid[i][y] == "#":
            ang = 90
            if not angle_vis[ang]:
                angle_vis[ang] += 1
                angles[ang].append((i, y))
            all_angles[ang].append((i, y))

    # down
    for i in range(x + 1, len(grid)):
        if grid[i][y] == "#":
            ang = 270
            if not angle_vis[ang]:
                angle_vis[ang] += 1
                angles[ang].append((i, y))
            all_angles[ang].append((i, y))

    # left
    for j in range(y - 1, -1, -1):
        if grid[x][j] == "#":
            ang = 180
            if not angle_vis[ang]:
                angle_vis[ang] += 1
                angles[ang].append((x, j))
            all_angles[ang].append((x, j))

    # right
    for j in range(y + 1, len(grid[0])):
        if grid[x][j] == "#":
            ang = 0
            if not angle_vis[ang]:
                angle_vis[ang] += 1
                angles[ang].append((x, j))
            all_angles[ang].append((x, j))

    out = sum(angle_vis.values())
    return out, all_angles


def p1(grid):
    max_vis = float("-inf")
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == "#":
                n_visible, all_angs = find_visible(i, j, grid)
                if n_visible > max_vis:
                    max_vis = n_visible
                    best_pos = (i, j)
    return max_vis, best_pos, all_angs


def manh(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])


def get_firing_order(all_angles):
    final_order = []
    angles = all_angles.keys()

    final_order.extend(list(reversed(sorted(filter(lambda x: 0 <= x <= 90, angles)))))
    final_order.extend(list(reversed(sorted(filter(lambda x: 270 <= x < 360, angles)))))
    final_order.extend(list(reversed(sorted(filter(lambda x: 180 <= x < 270, angles)))))
    final_order.extend(list(reversed(sorted(filter(lambda x: 90 < x < 180, angles)))))
    return final_order


def p2(grid, start):
    _, all_angs = find_visible(start[0], start[1], grid)
    order = get_firing_order(all_angs)

    # sort by distance
    for ang in all_angs.keys():
        all_angs[ang] = sorted(all_angs[ang], key=lambda x: manh(start, x))

    fire_idx = 0
    count = 0
    vaporized = []
    while count < 200:
        fire_idx %= len(order)
        angle = order[fire_idx]
        candidates = all_angs[angle]
        if not candidates:
            fire_idx += 1
            continue
        else:
            cand = candidates.pop(0)
            fire_idx += 1
            count += 1
            vaporized.append(cand)

    last_cand = vaporized[-1]
    return 100 * last_cand[1] + last_cand[0]


def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time
    start = time()

    answer_a, answer_b = None, None
    grid = parse(filename)
    answer_a, best_pos, all_angs = p1(grid)

    if "sample2" in filename:
        best_pos = (3, 8)
    answer_b = p2(grid, best_pos)
    # run_program(intcode, inp=5)
    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 210
    sample_b_answer = 802

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
        submit_answer(answer_a, "a", day=10, year=2019)
    except AocdError:
        submit_answer(answer_b, "b", day=10, year=2019)

