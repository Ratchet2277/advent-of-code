import re
from common import read_file

if __name__ != '__main__':
    raise Exception('This file is not meant to be imported')


def main():
    input_path = "./input.txt"
    regex = re.compile(r'(\d+)\s+(\d+)')
    first_list, second_list = get_input(input_path, regex)

    first_list.sort()
    second_list.sort()

    result_list = compare_list(first_list, second_list)

    print('Total distance part one: ', sum(result_list))
    print('Total distance part two: ', part_two(first_list, second_list))


def get_input(path: str, matching_regex: re) -> (list, list):
    input = read_file(path)

    first_list = []
    second_list = []

    for line in input:
        result = re.findall(matching_regex, line)
        first_list.append(int(result[0][0]))
        second_list.append(int(result[0][1]))

    return first_list, second_list


def compare_list(first_list: list, second_list: list) -> list:
    result_list = []
    for i in range(len(first_list)):
        result_list.append(abs(first_list[i] - second_list[i]))
    return result_list


def part_two(first_list: list[int], second_list: list[int]) -> int:
    total = 0
    for number in first_list:
        multiplier = second_list.count(number)
        total += number * multiplier
    return total


main()
