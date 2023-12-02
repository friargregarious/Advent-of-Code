"""
###############################################################################
#
#                              ADVENT OF CODE: 2023
#                                  Trebuchet?!
#                      https://adventofcode.com/2023/day/1
#
###############################################################################
#
# SOLVER:   friargregarious (greg.denyes@gmail.com)
# SOLVED:   {#SOLVED}
# HOME:     https://github.com/friargregarious
# SOURCE:   https://github.com/friargregarious/AOC-2023
#
# WRITTEN AND TESTED IN PYTHON VER 3.11.6
#
###############################################################################
"""
###############################################################################
# imports, globals and helper functions/classes

import os
from num2words import num2words as n2w
import logger

os.system("cls")
log = logger.Logger("advent_2003_1_b.log")
log.submit(f"LOGGER INITIATED")
report = logger.Logger("check_answers.txt")


def data(source_text_stream: str = "input.txt"):
    """
    flake8 suggested a generator instead of a list comprehension.
    I'm starting to get annoyed by all the 'helpful' code suggestiongs
    """
    text_source_list = []
    if source_text_stream in ["input.txt", "example.txt"]:
        log.submit(f"DATA RECEIVED: {source_text_stream}")
        with open(source_text_stream, mode="r", encoding="UTF-8") as file:
            text_source_list = list(file.read()[:-1].split("\n"))
    else:
        log.submit("DATA RECEIVED: raw text, likely from aocd.submit")
        # this is the case where the raw text is fed to the generator
        # by the aocd.submit() package
        text_source_list = list(str(source_text_stream).split("\n"))

    return text_source_list


class CalibrationValue:
    """class doc placeholder"""

    nums = [(str(x), n2w(x)) for x in range(10)]

    def __init__(self, original):
        """method doc placeholder"""
        if not isinstance(original, str):
            raise TypeError("CalibrationValue takes str only.")
        log.submit(f"CALVAL INITIATED: {original}")

        if len(original) > 0:
            self.original = original
        else:
            raise EOFError("Blank Line submitted to CAL VAL")

    def digit_str(self, part="A"):
        """method doc placeholder"""
        result = ""
        if part == "A":
            sort_key = sorted(self.ints_indexes.keys())
            for key in sort_key:
                result += self.ints_indexes[key]
        else:
            sort_key = sorted(self.all_numbers.keys())
            for key in sort_key:
                result += self.all_numbers[key]

        log.submit(f"CALVAL.digit_str({self.original}) RETURNS: {result}")

        return result

    @property
    def all_numbers(self):
        """method doc placeholder"""
        temp = self.ints_indexes
        temp.update(self.words_indexes)

        log.submit(f"CALVAL.all_numbers({self.original}) RETURNS: {temp}")
        return temp

    def value(self, part="A"):
        """returns only the first and last digit in a digits_str"""
        # s = int(digits_str[0] + digits_str[-1])
        # report[i][part]["relevant"] = s

        digit_str = str(self.digit_str(part))

        if part == "A" and len(digit_str) == 0:
            relevant_value = 0
        else:
            relevant_value = int(digit_str[0] + digit_str[-1])

        log.submit(
            f"CALVAL.value({self.original}, part={part}) RETURNS: {relevant_value}"
        )
        return relevant_value
        # return int(self.all_numbers[0] + self.all_numbers[-1])

    @property
    def total_ints(self):
        """method doc placeholder"""
        counts = [self.original.count(x[0]) for x in self.nums]
        log.submit(f"CALVAL.total_ints({self.original}) RETURNS: {sum(counts)}")
        return sum(counts)

    @property
    def total_words(self):
        """method doc placeholder"""
        counts = [self.original.count(x[1]) for x in self.nums]
        log.submit(f"CALVAL.total_words({self.original}) RETURNS: {sum(counts)}")

        return sum(counts)

    @property
    def ints_indexes(self):
        """method doc placeholder"""
        found = {}
        for i, char in enumerate(self.original):
            if char.isnumeric():
                found[i] = char

        log.submit(f"CALVAL.ints_indexes({self.original}) RETURNS: {found.items()}")
        return found

    @property
    def words_indexes(self):
        """method doc placeholder"""
        found = {}
        for num_int, num_word in self.nums:
            how_many = self.original.count(num_word)
            pointer = 0
            position = 0

            for _ in range(how_many):
                position = self.original[pointer:].find(num_word)
                # print(position, pointer, num_word, self.original[position:])
                found[pointer + position] = num_int
                pointer = position + 1

        log.submit(f"CALVAL.words_indexes({self.original}) RETURNS: {found.items()}")
        return found

    @property
    def report(self):
        """for viewing final answers"""
        return "".join(
            [
                self.digit_str("A").rjust(10, " "),
                self.original.center(20),
                self.digit_str("B"),
            ]
        )


###############################################################################
# PART A
###############################################################################
# The newly-improved calibration document consists of lines of text; each line
# originally contained a specific *calibration value* that the Elves now need
# to recover. On each line, the calibration value can be found by combining
# the *first digit* and the *last digit* (in that order) to form a single
# *two-digit number*.
#
# For example:
#
# 1abc2             = 12
# pqr3stu8vwx       = 38
# a1b2c3d4e5f       = 15
# treb7uchet        = 77
#                   -----
#                    142


class WorkList(list):
    """doc placeholder"""

    def __init__(self):
        """method doc placeholder"""
        # words = []

    def set_words(self, source_list):
        """method doc placeholder"""
        self.extend([CalibrationValue(line) for line in source_list if len(line) > 0])

    def solve(self, puzzle):
        """method doc placeholder"""
        return sum([word.value(puzzle) for word in self])

 

ALL_WORDS = WorkList()


def solve_a(source):
    """for solving Part A"""

    if len(ALL_WORDS) == 0:
        ALL_WORDS.set_words(source)

    log.submit(f"string length submitted to CALVAL Part B {len(source[0])}")
    solution = ALL_WORDS.solve("A")

    log.submit(f"solve_a() RETURNS: {solution}")
    for word in ALL_WORDS:
        report.submit(f"REPORT: {word.report}")
    return solution


###############################################################################
# PART B
###############################################################################
# Same as Part A, EXCEPT:
# we just need to replace numbers that are in the form of words:
# two1nine            29
# eightwothree        83
# abcone2threexyz     13
# xtwone3four         24
# 4nineeightseven2    42
# zoneight234         14
# 7pqrstsixteen       76

# In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76.
# Adding these together produces 281.


def solve_b(source):
    """for solving Part B"""

    if len(ALL_WORDS) == 0:
        ALL_WORDS.set_words(source)

    # log.submit(f"string length submitted to CALVAL Part B {len(source[0])}")
    solution = ALL_WORDS.solve("B")
    log.submit(f"solve_b() RETURNS: {solution}")
    for word in ALL_WORDS:
        report.submit(f"REPORT: {word.report}")
    return solution


###############################################################################
def main(source):
    """ENTRY POINT FOR SUBMITTING & BENCHMARKING"""
    solution_a = solve_a(source=data(source))
    solution_b = solve_b(source=data(source))

    if source.endswith(".txt"):
        msg = f"main({source}) RETURNS: ({solution_a}, {solution_b})"
    else:
        msg = f"main(Raw Text) RETURNS: ({solution_a}, {solution_b})"

    log.submit(msg)
    return (solution_a, solution_b)


###############################################################################
# for testing in development
if __name__ == "__main__":
    # TEST_WITH = "input.txt"
    log.set_behaviours(print2screen=True, inturrupts=False)
    TEST_WITH = str(open("example.txt").read())
    part_a, part_b = main(TEST_WITH)

    for msg in log.report():
        print(msg)

    for row in report.report():
        print(row)
