"""
#        ADVENT OF CODE | 2016 | SECURITY THROUGH OBSCURITY | PART [A]        #
#                         adventofcode.com/2016/day/4                         #
# SOLVER: --------------------------------------------------- friargregarious #
# CONTACT: --------------------------------------- friar.gregarious@gmail.com #
# HOME: -------------------------------------------------------------- github #
# SOURCE: ----------------------------------- ~/Advent-of-Code/AOC 2016/Day 4 #
# WRITTEN AND TESTED IN: --------------------------------------------- 3.11.6 #
"""

###############################################################################
# IMPORTS #####################################################################
###############################################################################

import os
import argparse
from pathlib import Path
import my_utilities
from string import ascii_letters

# import math
# from datetime import datetime
# from termcolor import colored
# import aocd

###############################################################################
# DECLARATIONS ################################################################
###############################################################################
__year__ = 2016
__day__ = 4
__build__ = 30
__version__ = "0.0.30"
__example_answer__ = 1514
__run_on_example__ = False

###############################################################################
# GATHER_TOOLS ################################################################
###############################################################################


def parse_input(source: str):
    """For parsing source string into usable content"""
    return list(Path(source).read_text(encoding="utf-8").split("\n"))


###############################################################################
# SOLVE PART A ################################################################
###############################################################################


def solve_a(data):
    """For solving PART a of day 4's puzzle."""
    print(print_version())
    solution = 0

    # aaaaa-bbb-z-y-x-123[abxyz]
    # a-b-c-d-e-f-g-h-987[abcde]
    # not-a-real-room-404[oarel]
    # totally-real-room-200[decoy]

    for row in data:
        counts = {}
        new_counts = {}

        words = row.split("-")
        _right = words[-1]
        room_num = int(_right.split("[")[0])
        order = _right.split("[")[1].strip("]")

        for word in words[:-1]:
            for c in word:
                if c in ascii_letters:
                    if c in counts:
                        counts[c] += 1
                    else:
                        counts[c] = 1

        print(words[:-1], room_num, order)
        print("counts:", counts)

        for k, v in counts.items():
            if v in new_counts:
                new_counts[v] += k
            else:
                new_counts[v] = k

        new_counts = {k: "".join(sorted(v)) for k, v in new_counts.items()}
        key = sorted(set(counts.values()), reverse=True)

        new_counts = {k: new_counts[k] for k in key}
        print("new counts:", new_counts)

        new_order = ""
        for k, v in new_counts.items():
            new_order += v

        new_order = new_order[:5]
        print("Order Match:", new_order, order, new_order == order, "\n")
        if new_order == order:
            solution += room_num

    return solution


###############################################################################
# MAIN ENTRY POINT FOR SUBMITTING AND BENCHMARKING ############################
###############################################################################
def main(source):
    """Main entry point"""
    return solve_a(source)


###############################################################################
# RUNNING_FROM_HOME ###########################################################
###############################################################################


def print_version():
    fname = f"AOC {__year__} Day {__day__}"
    return f"Program: ({fname}) Version: {__version__} Build: {__build__:04}"


if __name__ == "__main__":
    os.system("cls")
    # parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(
        prog=f"{__file__}",
        description=f"Solves puzzle for inputs provided on AOC {__year__} Day {__day__}.",
        epilog="Only used within the AOC Enviroment.",
    )

    # parser.add_argument(
    #     "solve",
    #     help="A or B, Default Runs on A.",
    #     default="A",
    #     action=main())

    parser.add_argument(
        "-e",
        "--example",
        help="Run This Solve on example input. Default is regular input.",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "-v",
        "--version",
        help="Returns the current version of this file.",
        action="version",
        version=print_version(),
    )

    args = parser.parse_args()

    __run_on_example__ = args.example
    print(f"Run on example: {__run_on_example__}")
    my_utilities.version_increment(__file__, sml=1)

    if __run_on_example__:
        example_path = str(Path(__file__).parent / "example.txt")
        src = parse_input(example_path)
    else:
        input_path = str(Path(__file__).parent / "input.txt")
        src = parse_input(input_path)

    # print(f"Solving: {args.solve}")
    answer = main(source=src)
    print(answer)
    # my_utilities.solve_a()
