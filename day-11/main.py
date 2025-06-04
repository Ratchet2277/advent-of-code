from collections.abc import Callable
import shutil

import progressbar

class Rule:
    def __init__(self, condition: Callable[[int], bool], rule: Callable[[int], list[int]]):
        self.condition = condition
        self.rule = rule


def main():
    shutil.copy('input.txt', 'last-result.txt')
    for i in progressbar.progressbar(range(75)):
        blink()
        shutil.copy('output.txt', 'last-result.txt')
    with open("last-result.txt", "r") as file:
        count = 0
        while True:
            char = file.read(1)
            if not char:
                print(count)
                return None
            if char == " ":
                count += 1
rules = [
    Rule(lambda stone: not stone, lambda stone: [1]),
    Rule(lambda stone: not bool(len(str(stone)) % 2),
         lambda stone: split_stone(stone)),
    Rule(lambda _: True, lambda stone: [stone * 2024])
]

def blink() -> None:
    with open("last-result.txt", "r") as file, open("output.txt", "w") as output:
        stone = ""
        while True:
            char = file.read(1)
            if not char:
                if not stone:
                    return None
                output.write(f"{" ".join([str(x) for x in change_stone(int(stone))])} ")
                return None

            if char == " ":
                if not stone:
                    continue
                output.write(f"{" ".join([str(x) for x in change_stone(int(stone))])} ")
                stone = ""
                continue

            stone += char
        return None

def split_stone(stone: int) -> list[int]:
    stone = str(stone)
    length = len(stone) >> 1
    return [int(stone[:length]), int(stone[length:])]

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
