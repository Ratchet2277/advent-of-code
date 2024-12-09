import multiprocessing
from copy import deepcopy
from enum import Enum
from typing import Optional

import progressbar

import common


class Orientation(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class Position:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y


class Obstacle(Position):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)


class Guard(Position):
    def __init__(self, x: int, y: int, orientation: Orientation):
        super().__init__(x, y)
        self.orientation = orientation
        self.step_count: int = 0

    def rotate(self):
        match self.orientation:
            case Orientation.NORTH:
                self.orientation = Orientation.EAST
            case Orientation.EAST:
                self.orientation = Orientation.SOUTH
            case Orientation.SOUTH:
                self.orientation = Orientation.WEST
            case Orientation.WEST:
                self.orientation = Orientation.NORTH

    def __copy__(self):
        return Guard(self.x, self.y, self.orientation)


class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[None] * width for _ in range(height)]
        self.guard = None

    def add_obstacle(self, obstacle: Obstacle):
        self.grid[obstacle.x][obstacle.y] = obstacle

    def add_guard(self, guard: Guard):
        self.grid[guard.x][guard.y] = guard
        self.guard = guard

    def move_guard(self) -> bool:
        guard = self.guard
        next_x = guard.x + (
            1 if guard.orientation == Orientation.SOUTH else -1 if guard.orientation == Orientation.NORTH else 0)
        next_y = guard.y + (
            1 if guard.orientation == Orientation.EAST else -1 if guard.orientation == Orientation.WEST else 0)

        if next_x < 0 or next_x >= self.height or next_y < 0 or next_y >= self.width:
            self.guard.rotate()
            return False

        if self.grid[next_x][next_y] != None:
            self.guard.rotate()
            return True

        self.grid[guard.x][guard.y] = None
        self.grid[next_x][next_y] = guard

        self.guard.x = next_x
        self.guard.y = next_y
        self.guard.step_count += 1
        return True


def main():
    data = common.read_file("input.txt")
    grid = Grid(len(data), len(data[0]))

    for x in range(len(data)):
        for y in range(len(data[x])):
            match data[x][y]:
                case ".":
                    continue
                case "#":
                    grid.add_obstacle(Obstacle(x, y))
                case "^":
                    grid.add_guard(Guard(x, y, Orientation.NORTH))

    case_while_guard_stuck = 0

    _, positions = simulate_grid(deepcopy(grid))

    print("Original path will cover {} different positions".format(len(positions)))

    print("Testing new obstacle positions :")

    procs = []
    nb_case_while_guard_stuck = multiprocessing.Value('i', 0)

    for x, y in positions:
        new_grid = deepcopy(grid)
        new_grid.add_obstacle(Obstacle(x, y))

        proc = multiprocessing.Process(target=simulate_grid, args=(new_grid, nb_case_while_guard_stuck))
        procs.append(proc)
        proc.start()

    for proc in progressbar.progressbar(procs):
        proc.join()

    print(f"Case stuck: {nb_case_while_guard_stuck.value}")


def simulate_grid(grid: Grid, nb_case_while_guard_stuck: Optional[multiprocessing.Value] = None) -> (
bool, list[tuple[int, int]]):
    guard_positions = [(grid.guard.x, grid.guard.y, grid.guard.orientation)]
    while grid.move_guard():
        position = (grid.guard.x, grid.guard.y, grid.guard.orientation)
        if position in guard_positions:
            if not nb_case_while_guard_stuck is None:
                nb_case_while_guard_stuck.value += 1
            return True, set([(pos[0], pos[1]) for pos in guard_positions])
        guard_positions.append(position)
    return False, set([(pos[0], pos[1]) for pos in guard_positions])


if __name__ == '__main__':
    main()
