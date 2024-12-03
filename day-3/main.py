import re

import common

if __name__ != '__main__':
    raise Exception('This file is not meant to be imported')


def main():
    input_data = ''.join(common.read_file("input.txt"))

    # Should be possible to do it in one regex, if you can't figure out how, I'm curious
    mul_regex = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    do_regex = re.compile(r"do\(\)")
    dont_regex = re.compile(r"don't\(\)")

    do_index = get_all_match_index(do_regex, input_data)
    dont_index = get_all_match_index(dont_regex, input_data)

    total_first_part = 0
    total = 0

    for mul in mul_regex.finditer(input_data):
        mul_total = int(mul.group(1)) * int(mul.group(2))
        total_first_part += mul_total

        max_do = list(filter(lambda x: x < mul.start(), do_index))
        max_dont = list(filter(lambda x: x < mul.start(), dont_index))

        # Is there a "do()" match before this match
        if not max_do:
            continue

        # Is there a "don't()" match, and determine which of "do()" and "don't()" is closer
        if max_dont and max(max_do) < max(max_dont):
            continue

        total += mul_total

    print('Total first part: ', total_first_part)
    print('Total second part: ', total)


def get_all_match_index(regex: re, string: str) -> list[int]:
    output = []
    for match in regex.finditer(string):
        output.append(match.start())
    return output


main()
