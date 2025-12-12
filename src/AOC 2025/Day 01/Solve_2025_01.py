"""
################################################################################
#                                                                              #
#                          ADVENT OF CODE: 2025 DAY 1                          #
#                               Secret Entrance                                #
#                     https://adventofcode.com/2025/day/1                      #
#                                                                              #
################################################################################
#                                                                              #
# A SOLVED:   N/A                                                              #
# B SOLVED:   N/A                                                              #
# SOLVER:     friargregarious (greg.denyes@gmail.com)                          #
# HOME:       https://github.com/friargregarious                               #
#                                                                              #
#                   WRITTEN AND TESTED IN PYTHON VER 3.13.7                    #
#                                                                              #
################################################################################
"""

###############################################################################
# imports, globals and helper functions/classes

import os, argparse, toml, sys
from pickle import TRUE
import solve_utilities as su
from pathlib import Path


DO_EXAMPLE: bool
VERBOSE: bool


def data(input_text_path: Path = Path("input.txt")):

    if DO_EXAMPLE:
        input_text_path = Path("example_a.txt")

    text_source_list = input_text_path.read_text(encoding="UTF-8").split("\n")

    return text_source_list


###############################################################################
# PART A
###############################################################################


class Dial:
    dial_setting: int
    zero_count = 0

    def __init__(self, starts_at: int = 50) -> None:
        self.dial_setting = starts_at

    def parse_instruction(self, instruction: str):
        # direction, steps = instruction[0], int(instruction[1:])
        return int(instruction.replace("L", "-").replace("R", "+"))

    def turn_dial(self, steps: int):
        old_step = int(self.dial_setting)

        self.dial_setting = self.dial_setting + steps

        if self.dial_setting < 0:
            self.dial_setting += 100

        if self.dial_setting > 99:
            self.dial_setting -= 100

        if self.dial_setting == 0:
            self.zero_count += 1

        print(
            f"Dial from: {old_step:2d} | Turn: {steps:3d} | Dial to: {self.dial_setting:2d} | zero count: {self.zero_count}"
        )


def solve_a(source):
    """for solving Part A"""

    print("Part A") if VERBOSE else None

    mysafe = Dial()
    for instruction in source:
        mysafe.turn_dial(mysafe.parse_instruction(instruction))

    print(
        f"Current dial setting: {mysafe.dial_setting} | Zero count: {mysafe.zero_count}"
    )

    su.submit_result(PUZZLE, mysafe.dial_setting, "A", CONFIG)
    (mysafe.zero_count)


###############################################################################
# PART B
###############################################################################
def solve_b(source):
    """for solving Part B"""

    print("Part B") if VERBOSE else None

    return 0


###############################################################################
# command line interface
###############################################################################
if __name__ == "__main__":
    os.system("cls")

    # Collect command line arguments
    arguments = argparse.ArgumentParser()
    for arp, ark in su.ARGS_LIST:
        arguments.add_argument(*arp, **ark)
    args = arguments.parse_args()

    su.print_args(vars(args))

    # Load puzzle parameters
    config = toml.load(Path(".env"))

    DO_A, DO_B = not args.part_b, args.part_b
    DO_EXAMPLE = args.example
    VERBOSE = args.verbose

    # open puzzle info
    puzzle = su.open_puzzle(config)

    if args.discord:
        su.Discord(puzzle=puzzle, config=config)
        sys.exit()

    if args.refresh:
        su.refresh_readme(puzzle)
        sys.exit()

    if args.submit:
        p = "A" if DO_A else "B"

        f_ex = "(From Example)" if DO_EXAMPLE else "(From input)"
        source_input = (
            data(Path("example_a.txt")) if DO_EXAMPLE else data(Path("input.txt"))
        )
        print(
            f"Submitting {'Example' if DO_EXAMPLE else 'Answer'} {'B' if DO_A else 'B'} for Review..."
        )
        result = solve_a(source_input) if DO_A else solve_b(source_input)

        correct_msg = ""
        match f"{'EXPL' if DO_EXAMPLE else 'REAL'}, {p}":
            case "EXPL, A":
                correct_answer = puzzle.examples[0].answer_a
                # correct_answer = 13
            case "EXPL, B":
                correct_answer = puzzle.examples[0].answer_b
                # correct_answer = '34'
            case "REAL, A":
                correct_answer = puzzle.answer_a if puzzle.answered_a else "unknown"
            case "REAL, B":
                correct_answer = puzzle.answer_b if puzzle.answered_b else "unknown"
            case _:
                correct_answer = "unknown"

        compare = correct_answer == str(result)
        correct_msg = (
            f"IS CORRECT!! ({correct_answer})"
            if compare
            else f"IS NOT CORRECT ({correct_answer})"
        )

        print(f"Solution ({p}): {result} {correct_msg} {f_ex}")
        su.update_header(puzzle)
        os.system("black .")

        if not DO_EXAMPLE:
            su.submit_result(puzzle, result, p, config)
