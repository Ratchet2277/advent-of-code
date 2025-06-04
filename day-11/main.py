from collections.abc import Callable

import common
import progressbar

class Rule:
    def __init__(self, condition: Callable[[int], bool], rule: Callable):
        self.condition = condition
        self.rule = rule


def main():
    data = common.read_file("input.txt")[0]
    stones: list[int] = [int(x) for x in data.split(" ")]

    for _ in progressbar.progressbar(range(75)):
        stones = blink(stones)
    print(len(stones))

def get_rules() -> list[Rule]:
    return [
        Rule(lambda stone: stone == 0, lambda stone: [1]),
        Rule(lambda stone: len(str(stone)) % 2 == 0,
             lambda stone: [int(str(stone)[: len(str(stone)) // 2 ]), int(str(stone)[(len(str(stone)) // 2):])]),
        Rule(lambda stone: True, lambda stone: [stone * 2024])
    ]

def blink(stones: list[int]) -> list[int]:
    new_stones: list[int] = []
    for stone in stones:
        new_stones.extend(change_stone(stone))
    return new_stones

def change_stone(stone: int) -> list[int]:
    rules = get_rules()
    for rule in rules:
        if not rule.condition(stone):
            continue
        return rule.rule(stone)
    raise ValueError("No rule found for this stone")

if __name__ == '__main__':
        main()
else:
    raise Exception('This file is not meant to be imported')
