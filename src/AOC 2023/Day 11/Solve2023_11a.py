###############################################################################
#             ADVENT OF CODE | 2023 | COSMIC EXPANSION | PART [A]             #
#                         adventofcode.com/2023/day/11                        #
# SOLVER: -------------------------------------------------- friargregarious #
# CONTACT: -------------------------------------- friar.gregarious@gmail.com #
# HOME: ------------------------------------------------------------- github #
# SOURCE: --------------------------------- ~/Advent-of-Code/AOC 2023/Day 11 #
# WRITTEN AND TESTED IN: -------------------------------------------- 3.11.6 #
###############################################################################
# IMPORTS #####################################################################
###############################################################################

import os
import my_utilities

# from my_utilities import MyConfigParser as MyCfg
import math
from datetime import datetime
from termcolor import colored
import aocd

###############################################################################
# DECLARATIONS ################################################################
###############################################################################

__version__ = "0.0.7"
__example_answer__ = 374
__run_on_example__ = True

###############################################################################
# GATHER_TOOLS ################################################################
###############################################################################


def parse_input(source: str = "input.txt") -> list:
    """For parsing source string into usable content"""

    if source.endswith(".txt"):
        galaxy = open(source, "r", encoding="utf-8").read()
        return galaxy

    return source.split()


def galaxy_expansion(source_map):
    # look for entire rows of "."
    working_galaxy = []
    max_wide = len(source_map[0])
    blank_cols = set()

    for row in source_map:
        working_galaxy.append(row)
        if str(row).count("#") <= 0:
            working_galaxy.append(row)
        else:
            for i, symbol in enumerate(row):
                if symbol == "#":
                    blank_cols.add(i)
                

    # for the example, blank_cols should = [2, 5, 8]

    print(blank_cols)


###############################################################################
# SOLVE PART A ################################################################
###############################################################################


def solve_a(data):
    """For solving PART a of day 11's puzzle."""
    expanded = galaxy_expansion(data)

    solution = 0
    return solution


###############################################################################
# MAIN ENTRY POINT FOR SUBMITTING AND BENCHMARKING ############################
###############################################################################


def main(source, example_answer:str="a"):
    """Main entry point"""
    solution = solve_a(source)
    return solution


###############################################################################
# RUNNING_FROM_HOME ###########################################################
###############################################################################

if __name__ == "__main__":
    my_utilities.version_increment(__file__, sml=1)
    if __run_on_example__:
        answer = main(parse_input("example.txt"), __example_answer__)
    else:
        answer = main(parse_input("input.txt"))
    my_utilities.version_increment(__file__, sml=1)
    # my_utilities.solve_me(answer, "a")
