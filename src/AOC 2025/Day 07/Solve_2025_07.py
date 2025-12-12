"""
################################################################################
#                                                                              #
#                          ADVENT OF CODE: 2025 DAY 7                          #
#                                 Laboratories                                 #
#                     https://adventofcode.com/2025/day/7                      #
#                                                                              #
################################################################################
#                                                                              #
# A SOLVED:   2025-12-07 18:31                                                 #
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

import enum
import json
import os, argparse, toml, sys
import time
import solve_utilities as su
from pathlib import Path


def data(input_text_path: Path = Path("input.txt")):

    text_source_list = input_text_path.read_text(encoding="UTF-8").split("\n")

    # return text_source_list
    return [[x for x in row] for row in text_source_list]


###############################################################################
# PART A
###############################################################################
def solve_a(source):
    """for solving Part A"""

    print("Part A") if VERBOSE else None

    SPLITS = 0

    for row in range(1, len(source)):
        for col in range(len(source[row])):

            if source[row][col] == "^" and source[row - 1][col] in ["S", "|"]:
                source[row][col] = "|"

            if source[row][col] == "^" and source[row - 1][col] == "|":
                SPLITS += 1
                source[row][col - 1 : col + 2] = "|^|"

    for row in source:
        print("".join(row))

    return SPLITS


###############################################################################
# PART B
###############################################################################


def solve_b(source):
    """for solving Part B"""
    print("Part B") if VERBOSE else None

    for row in range(1, len(source)):
        for col in range(len(source[row])):

            if source[row][col] != "^" and source[row - 1][col] in ["S", "|"]:
                source[row][col] = "|"

            if source[row][col] == "^" and source[row - 1][col] == "|":
                source[row][col - 1 : col + 2] = "|^|"

    

    for row in source:
        print("".join(row))

    this = ""
    for row in range(len(source)):
        for col in range(len(source[row])):
            this += source[row][col]
        this += "\n"

    Path("timeline.txt").write_text(this, encoding="utf-8")



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
        result = solve_a(source_input) if DO_A else solve_b(source_input)

        correct_msg = ""
        match f"{'EXPL' if DO_EXAMPLE else 'REAL'}, {p}":
            case "EXPL, A":
                correct_answer = puzzle.examples[0].answer_a
            case "EXPL, B":
                correct_answer = puzzle.examples[0].answer_b
            # case "EXPL, B": correct_answer = '34' # puzzle file is corrupt.
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
