from collections.abc import Callable
import common

import progressbar

class Rule:
    def __init__(self, condition: Callable[[int], bool], rule: Callable[[int], list[int]]):
        self.condition = condition
        self.rule = rule

cache: dict[int, list[int]] = {}

def main():
    data = common.read_file("input.txt")[0]
    data = [int(x) for x in data.split(" ")]
    sorted_data: dict[int, int] = {}

    for stone in data:
        if stone not in sorted_data.keys():
            sorted_data[stone] = 1
            continue
        sorted_data[stone] += 1

    for _ in progressbar.progressbar(range(75)):
        sorted_data = blink(sorted_data)
    print(sum(sorted_data.values()))
    print(len(sorted_data))

rules = [
    Rule(lambda stone: not stone, lambda stone: [1]),
    Rule(lambda stone: not bool(len(str(stone)) % 2),
         lambda stone: split_stone(stone)),
    Rule(lambda _: True, lambda stone: [stone * 2024])
]

def blink(stones: dict[int, int]) -> dict[int, int]:
    new_stones = {}
    for value in stones:
        for stone in change_stone(value):
            if stone not in new_stones.keys():
                new_stones[stone] = stones[value]
                continue
            new_stones[stone] += stones[value]
    return new_stones

def split_stone(stone: int) -> list[int]:
    stone = str(stone)
    length = len(stone) >> 1
    return [int(stone[:length]), int(stone[length:])]

def change_stone(stone: int) -> list[int]:
    if stone in cache:
        return cache[stone]
    for rule in rules:
        if not rule.condition(stone):
            continue
        cache[stone] = rule.rule(stone)
        return cache[stone]
    raise ValueError("No rule found for this stone")

if __name__ == '__main__':
        main()
else:
    raise Exception('This file is not meant to be imported')
