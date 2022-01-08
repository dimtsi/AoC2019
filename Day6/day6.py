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

def parse(filename: str) -> Tuple:
    orbits = defaultdict(list)
    graph = defaultdict(list)
    with open(filename, "r") as f:
        lines = f.read().split("\n")

        for line in lines:
            a, b = line.split(")")
            orbits[b].append(a)
            orbits[a]
            graph[a].append(b)
            graph[b].append(a)
    return orbits, graph


def explore(node, orbits):
    count = 0
    stack = [node]
    while stack:
        curr = stack.pop()
        if curr != "COM":
            for neigh in orbits[curr]:
                stack.append(neigh)
                count += 1
    return count



def get_total_conns(orbits: DefaultDict[str, List]):
    total_count = 0
    stack = [*orbits.keys()]

    while stack:
        elem = stack.pop()
        total_count += explore(elem, orbits)

    return total_count


def dfs(G, start, end, curr_path):
    for neigh in G[start]:
        if neigh == end:
            PATHS_TO_END.append(curr_path + [end])
        elif neigh in curr_path:
            continue
        else:
            dfs(G, neigh, end, curr_path + [neigh])


def find_path_to_santa(orbits, G):
    start = orbits["YOU"][0]
    end = orbits["SAN"][0]
    orbits.pop("YOU")
    orbits.pop("SAN")

    dfs(G, start, end, [start])
    shortest_path = sorted(PATHS_TO_END, key=len)[0]
    return len(shortest_path) - 1




def main(filename: str) -> Tuple[Optional[int], Optional[int]]:
    from time import time

    global PATHS_TO_END

    PATHS_TO_END = []

    start = time()
    answer_a, answer_b = None, None
    orbits, _ = parse(filename)
    answer_a = get_total_conns(orbits)
    # #p2
    if "sample" in filename:
        filename = "sample2.txt"
    orbits, g = parse(filename)
    answer_b = find_path_to_santa(orbits, g)
    # run_program(intcode, inp=5)
    end = time()
    print(end - start)
    return answer_a, answer_b


if __name__ == "__main__":

    from utils import submit_answer
    from aocd.exceptions import AocdError

    sample = "sample.txt"
    input = "input.txt"

    sample_a_answer = 42
    sample_b_answer = 4

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
        submit_answer(answer_a, "a", day=6, year=2019)
    except AocdError:
        submit_answer(answer_b, "b", day=6, year=2019)

