from copy import copy
from typing import Optional

import progressbar

import common


def main():
    disk_map: str = common.read_file("input.txt")[0]
    disk = []

    is_free_space = False
    file_id = 0
    for number in disk_map:
        disk += [None if is_free_space else file_id] * int(number)
        file_id += int(not is_free_space)
        is_free_space = not is_free_space

    part_1_disk = compact_disk_part_1(copy(disk))
    part_2_disk = compact_disk_part_2(copy(disk))

    print("Part 1 Checksum:", sum([number * i for i, number in enumerate(part_1_disk) if number is not None]))
    print("Part 2 Checksum:", sum([number * i for i, number in enumerate(part_2_disk) if number is not None]))


def compact_disk_part_2(disk: list[Optional[int]]) -> list[Optional[int]]:
    current_file_id = None
    file_length = 0
    for i in progressbar.progressbar(range(len(disk) - 1, 0, -1), redirect_stdout=True):

        if disk[i] is None and current_file_id is None:
            continue
        if current_file_id is None:
            current_file_id = disk[i]

        if disk[i] == current_file_id:
            file_length += 1
            continue

        free_space = 0
        for j in range(disk.index(None), len(disk)):
            # thx to u/the_cassiopeia whose solution indirectly helped to find an error here
            if i < j:
                break

            if disk[j] is not None:
                free_space = 0
                continue
            free_space += 1

            if free_space < file_length:
                continue

            disk[j + 1 - file_length: j + 1] = [current_file_id] * file_length
            disk[i + 1: i + 1 + file_length] = [None] * file_length
            break

        current_file_id = disk[i]
        file_length = 0 if disk[i] is None else 1
    return disk


def compact_disk_part_1(disk: list[Optional[int]]) -> list[Optional[int]]:
    print("Compacting data:")
    for i in progressbar.progressbar(range(len(disk) - 1, 0, -1), redirect_stdout=True):
        if disk[i] is None:
            continue
        for j, free_space in enumerate(disk):
            if free_space is None:
                disk[j], disk[i] = disk[i], None
                break
            if i == j:
                return disk


if __name__ == '__main__':
    main()
