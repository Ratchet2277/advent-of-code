import concurrent.futures
from collections.abc import Callable

import common
import progressbar

class Rule:
    def __init__(self, condition: Callable[[int], bool], rule: Callable[[int], list[int]]):
        self.condition = condition
        self.rule = rule


def main():
    data = common.read_file("input.txt")[0]
    stones: list[int] = [int(x) for x in data.split(" ")]

    for _ in progressbar.progressbar(range(75)):
        stones = blink(stones)
    print(len(stones))

rules = [
    Rule(lambda stone: not stone, lambda stone: [0]),
    Rule(lambda stone: not bool(len(str(stone)) % 2),
         lambda stone: split_stone(stone)),
    Rule(lambda _: True, lambda stone: [stone * 2024])
]

def blink(stones: list[int]) -> list[int]:
    new_stones = []
    for stone in stones:
        new_stones.extend(change_stone(stone))

    return new_stones

def split_stone(stone: int) -> list[int]:
    stone = str(stone)
    length = len(stone) >> 1
    return [int(stone[:length]), int(stone[length:])]

def change_stone_batch(stones: list[int]) -> list[int]:
    new_stones = []
    for stone in stones:
        new_stones.extend(change_stone(stone))
    return new_stones

def change_stone(stone: int) -> list[int]:
    for rule in rules:
        if not rule.condition(stone):
            continue
        return rule.rule(stone)
    raise ValueError("No rule found for this stone")

if __name__ == '__main__':
        main()
else:
    raise Exception('This file is not meant to be imported')
