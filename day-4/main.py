import common

if __name__ != '__main__':
    raise Exception('This file is not meant to be imported')


def main():
    matrix = common.read_file("input.txt")
    matrix = common.strip_end_of_line(matrix)
    part_one(matrix)
    part_two(matrix)


def part_one(matrix: list[str]):
    original_matrix = matrix

    total_count = count_in_matrix(matrix)
    print("Horizontal :", total_count)

    matrix = rotate_matrix(matrix)
    total_count += count_in_matrix(matrix)
    print("With Vertical :", total_count)

    matrix = diagonal_matrix(matrix)
    total_count += count_in_matrix(matrix)
    print("With Diag :", total_count)

    matrix = diagonal_matrix(original_matrix)
    total_count += count_in_matrix(matrix)
    print("With Diag 2 :", total_count)


def part_two(matrix: list[str]):
    count = 0
    for x in range(len(matrix) - 2):
        for y in range(len(matrix[x]) - 2):
            sub_matrix = matrix[x:x + 3]
            sub_matrix = [line[y: y + 3] for line in sub_matrix]
            if is_sub_matrix_x_mas(sub_matrix):
                count += 1
    print("X-MAS count: ", count)


def is_sub_matrix_x_mas(sub_matrix: list[str]) -> bool:
    if sub_matrix[1][1] != 'A':
        return False

    for orientation in range(4):
        if orientation:
            sub_matrix = rotate_matrix(sub_matrix)
        if test_orientation(sub_matrix):
            return True

    return False


def test_orientation(sub_matrix: list[str]) -> bool:
    match = 'MAS'

    for i in range(3):
        if sub_matrix[i][i] != match[i] or sub_matrix[2 - i][i] != match[i]:
            return False
    return True


def count_xmas(line: str) -> int:
    lookup_string = 'XMAS'
    return line.count(lookup_string) + invert_line(line).count(lookup_string)


def count_in_matrix(matrix: list[str]) -> int:
    count = 0
    for line in matrix:
        count += count_xmas(line)
    return count


def invert_line(line: str) -> str:
    return line[::-1]


def rotate_matrix(lines: list[str]) -> list[str]:
    output = list(zip(*lines[::-1]))

    return [''.join(line) for line in output]


def diagonal_matrix(lines: list[str]) -> list[str]:
    output = []
    max_line = len(lines)
    max_col = max(len(x) for x in lines)

    for i in range(max_line + max_col):
        line = []
        for x in range(i + 1):
            y = i - x
            if x >= max_line:
                break
            if y >= max_col:
                continue
            line.append(lines[x][y])
        output.append(''.join(line))

    return output


main()
