###############################################################################
#               ADVENT OF CODE | 2023 | LENS LIBRARY | PART [A]               #
#                         adventofcode.com/2023/day/15                        #
# SOLVER: --------------------------------------------------- friargregarious #
# CONTACT: --------------------------------------- friar.gregarious@gmail.com #
# HOME: -------------------------------------------------------------- github #
# SOURCE: ---------------------------------- ~/Advent-of-Code/AOC 2023/Day 15 #
# WRITTEN AND TESTED IN: --------------------------------------------- 3.11.6 #
###############################################################################
# IMPORTS #####################################################################
###############################################################################

from importlib.abc import SourceLoader
import os

#  from my_utilities import MyConfigParser as MyCfg
import my_utilities

# import math
# from datetime import datetime
from termcolor import colored

# import aocd

###############################################################################
# DECLARATIONS ################################################################
###############################################################################

__version__ = "0.0.46"
__example_answer__ = 1320
__run_on_example__ = False
__verbose__ = False

###############################################################################
# GATHER_TOOLS ################################################################
###############################################################################


def parse_input(source: str = "inputs.txt") -> list:
    """For parsing source string into usable content"""

    if source.endswith(".txt"):
        return open(source).read().split(",")
    return source.split(",")


def hash(c_val, char_val):
    ch_ord = ord(char_val)
    if __verbose__:
        print(f"   Previous Value was {colored(c_val, 'blue')}")
        # ((c_val + ord(ch_ord)) ** 2) % 256
        print(f"\tStep 1 - ascii of '{char_val}' is {colored(ch_ord, 'green')}")

        print(
            f"\tStep 2 - Current Val '{colored(c_val, 'blue')}' + {colored(ch_ord, 'green')} = {colored(c_val+ch_ord, 'yellow')}"
        )

    c_val += ch_ord

    if __verbose__:
        print(
            f"\tStep 3 - Current Val '{colored(c_val, 'yellow')}' * 17 = {colored(c_val * 17, 'red')}"
        )

    c_val *= 17

    if __verbose__:
        print(
            f"\tStep 4 - Current Val {colored(c_val,'red')} / 256 leaves a remainder of '{colored(c_val % 256,'blue')}'"
        )
    c_val %= 256

    return c_val


###############################################################################
# SOLVE PART A ################################################################
###############################################################################


def solve_a(data, ex_ans=0):
    """For solving PART a of day 15's puzzle."""

    hashes = []
    for item in data:
        this_hash = 0
        if __verbose__:
            print(f"New Phrase: {colored(item, 'magenta')}")

        for char in item:
            this_hash = hash(this_hash, char)
        hashes.append(this_hash)

    solution = sum(hashes)

    if __run_on_example__:
        print(f"I got {solution} and it matches {ex_ans}: {solution == ex_ans}.")
        assert solution == ex_ans
    return solution


###############################################################################
# MAIN ENTRY POINT FOR SUBMITTING AND BENCHMARKING ############################
###############################################################################


def main(source):
    """Main entry point"""
    if __run_on_example__:
        return solve_a(parse_input("example.txt"), __example_answer__)
    return solve_a(parse_input(source))


###############################################################################
# RUNNING_FROM_HOME ###########################################################
###############################################################################

if __name__ == "__main__":
    os.system("cls")
    my_utilities.version_increment(__file__, sml=1)
    # __verbose__ = True
    # __run_on_example__ = True
    answer = main("inputs.txt")
    my_utilities.version_increment(__file__, sml=1)
    my_utilities.solve_a(answer)
