from typing import Dict

import common


def main():
    data = common.read_file('input.txt')
    data = common.strip_end_of_line(data)
    max_size = (len(data), len(data[0]))
    antennas = parse_data(data)

    # using set() instead of list() cause it filter duplicate by itself
    antinodes = set()
    part1_antinodes = set()
    for frequency in antennas:
        antinodes = antinodes.union(get_anti_nodes_for_frequency(antennas[frequency], max_size))
        part1_antinodes = part1_antinodes.union(get_anti_nodes_for_frequency(antennas[frequency], max_size, True))

    print(len(part1_antinodes))
    print(len(antinodes))


def parse_data(data: list[str]) -> Dict[chr, list[tuple[int, int]]]:
    output = {}
    for x, line in enumerate(data):
        for y, char in enumerate(line):
            if char == ".":
                continue
            if not char in output.keys():
                output[char] = []
            output[char].append((x, y))

    return output


def get_anti_nodes_for_frequency(antennas: list[tuple[int, int]], max_size: tuple[int, int], is_part_1: bool = False) -> \
        set[tuple[int, int]]:
    antinodes = set()

    for i, node1 in enumerate(antennas):
        for node2 in antennas[i + 1:]:
            antinodes = antinodes.union(get_antinodes_for_pair(node1, node2, max_size, is_part_1))
    return antinodes


def get_antinodes_for_pair(node1: tuple[int, int], node2: tuple[int, int], max_size: tuple[int, int],
                           is_part_1: bool = False) -> set[tuple[int, int]]:
    delta_x, delta_y = node1[0] - node2[0], node1[1] - node2[1]
    antinodes = set()
    if not is_part_1:
        antinodes.add(node1)

    # Used two loop for readable and simplification issue, could also be done through i and -i in calculation, break the loop when both are out of grid
    # positive side
    i = 1
    while True:
        antinode = (node1[0] + delta_x * i, node1[1] + delta_y * i)
        if not is_node_in_grid(antinode, max_size):
            break
        antinodes.add(antinode)
        i += 1
        if is_part_1:
            break

    if not is_part_1:
        # if it's part 1 solution, use i = 2 form the previous loop, since i=1 would give node2 coordinate which is only needed in part 2
        # initial part 1 solution was to use node2 coordinate in calculation instead of node1 but turn out to better fit both solution easily with this one
        i = 1

    # negative side
    while True:
        antinode = (node1[0] - delta_x * i, node1[1] - delta_y * i)
        if not is_node_in_grid(antinode, max_size):
            break
        antinodes.add(antinode)
        if is_part_1:
            break
        i += 1

    return antinodes


def is_node_in_grid(node: tuple[int, int], max_size: tuple[int, int]) -> bool:
    if node[0] >= max_size[0] or node[1] >= max_size[1]:
        return False
    if node[0] < 0 or node[1] < 0:
        return False
    return True


if __name__ == '__main__':
    main()
