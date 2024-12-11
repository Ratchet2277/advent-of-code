import common

def main():
    grid = common.strip_end_of_line(common.read_file("input.txt"))
    total_score = 0
    part_1_score = 0
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if int(grid[y][x]) != 0:
                continue
            trail = follow_trail(grid, x, y)
            total_score += len(trail)
            part_1_score += len(set(trail))
    print(part_1_score)
    print(total_score)

def follow_trail(grid: list[str], x: int, y: int) -> list[tuple[int, int]]:
    current_value = int(grid[y][x])
    if current_value == 9:
        return [(x, y)]

    output = list()
    for neighbor in get_neighborhood_coord(x, y):
        if (neighbor[0], neighbor[1]) in output:
            continue
        if neighbor[0] < 0 or neighbor[1] < 0:
            continue
        if neighbor[0] >= len(grid[0]) or neighbor[1] >= len(grid):
            continue
        next_value = int(grid[neighbor[1]][neighbor[0]])
        if next_value != (current_value + 1):
            continue
        output += follow_trail(grid, neighbor[0], neighbor[1])
    return output



def get_neighborhood_coord(x: int, y: int)-> list[tuple[int, int]]:
    return [(x-1, y), (x, y-1), (x, y+1), (x+1, y)]


if __name__ == '__main__':
    main()