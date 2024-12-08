import ctypes
import multiprocessing
from multiprocessing import Process
from operator import concat
from typing import Self, Optional

import gmpy2
import progressbar

import common


class Equation:
    def __init__(self, solution: int, numbers: list[int]):
        self.solution = solution
        self.numbers = numbers

    def __str__(self):
        return f'Solution: {self.solution}, Numbers: {self.numbers}'


class Solution(Equation):
    symboles = {
        0: "+",
        1: "*",
        2: "||"
    }

    def __init__(self, solution: int, numbers: list[int]):
        super().__init__(solution, numbers)
        self.symboles = []

    @staticmethod
    def from_equation(equation: Equation) -> 'Solution':
        return Solution(equation.solution, equation.numbers)

    def set_solution(self, symboles: list[chr]) -> Self:
        self.symboles = symboles
        return self

    def test_solution(self) -> bool:

        if self.__eval_formula(self.numbers, self.symboles, self.solution) == self.solution:
            return True

        return False

    @staticmethod
    def __eval_formula(numbers: list[int], symboles: list[chr], max: int) -> int:
        if len(numbers) - 1 != len(symboles):
            raise Exception('Number of numbers and symbols do not match')
        second_number = numbers[-1]
        symbole = symboles[-1]

        if len(numbers) > 2:
            first_number = Solution.__eval_formula(numbers[:-1], symboles[:-1], max)
            if first_number > max:
                return 0
        else:
            first_number = numbers[0]

        if symbole not in symboles:
            raise Exception(f'Symbole {symbole} not in {symboles}')

        # since concat use "+" un python too, that case need to be handled manually
        if symbole == '||':
            result = str(concat(str(first_number), str(second_number)))
            return int(result)

        return int(eval(str(first_number) + symbole + str(second_number)))

    def get_string_formula(self) -> Optional[str]:
        if len(self.symboles) != len(self.numbers) - 1:
            return None

        formula = str(self.numbers[0])
        for index, number in enumerate(self.numbers[1:]):
            addition = str(self.symboles[index]) + str(number)
            formula = formula + addition

        return formula

    def __str__(self) -> str:
        return self.get_string_formula() + " = " + str(self.solution)


def main():
    data = common.read_file("input.txt")
    equations = [parse_equation(line) for line in data if line.index(':')]

    procs = []

    summed_solutions = multiprocessing.Value(ctypes.c_int64, 0)

    for equation in equations:
        proc = Process(target=solve_equation, args=(equation, summed_solutions))
        procs.append(proc)
        proc.start()

    for proc in progressbar.progressbar(procs):
        proc.join()

    print(str(summed_solutions.value))


def parse_equation(equation: str) -> Equation:
    solution, numbers = equation.split(':')
    numbers = [int(number) for number in numbers.split(' ') if len(number)]
    return Equation(int(solution), numbers)


def convert_digits_to_symboles(digits: str) -> list[chr]:
    output = []
    for digit in digits:
        output.append(Solution.symboles[int(digit)])

    return output


def solve_equation(equation: Equation, summed_solutions: multiprocessing.Value) -> None:
    nb_symboles = len(equation.numbers) - 1
    nb_possibilities = len(Solution.symboles) ** nb_symboles
    for possibility in range(nb_possibilities):
        digits = gmpy2.digits(possibility, len(Solution.symboles)).rjust(nb_symboles, '0')
        symboles = convert_digits_to_symboles(digits)
        solution = Solution.from_equation(equation).set_solution(symboles)
        if solution.test_solution():
            summed_solutions.value += solution.solution
            return


if __name__ == "__main__":
    main()
