"""
#               ADVENT OF CODE | 2023 | STEP COUNTER | PART [A]               #
#                         adventofcode.com/2023/day/21                        #
# SOLVER: --------------------------------------------------- friargregarious #
# CONTACT: --------------------------------------- friar.gregarious@gmail.com #
# HOME: -------------------------------------------------------------- github #
# SOURCE: ---------------------------------- ~/Advent-of-Code/AOC 2023/Day 21 #
# WRITTEN AND TESTED IN: --------------------------------------------- 3.11.6 #
"""
###############################################################################
# IMPORTS #####################################################################
###############################################################################

import os

#  from my_utilities import MyConfigParser as MyCfg
import my_utilities

# import math
# from datetime import datetime
# from termcolor import colored
# import aocd

###############################################################################
# DECLARATIONS ################################################################
###############################################################################

__version__ = "0.0.0"
__example_answer__ = 64
__run_on_example__ = False

###############################################################################
# GATHER_TOOLS ################################################################
###############################################################################


def parse_input(source: str = "input.txt") -> list:
    """For parsing source string into usable content"""
    pass


###############################################################################
# SOLVE PART A ################################################################
###############################################################################


def solve_a(data):
    """For solving PART a of day 21's puzzle."""
    solution = data

    return solution


###############################################################################
# MAIN ENTRY POINT FOR SUBMITTING AND BENCHMARKING ############################
###############################################################################


def main(source):
    """Main entry point"""
    if __run_on_example__:
        return solve_a("example.txt", __example_answer__)
    return solve_a(source)


###############################################################################
# RUNNING_FROM_HOME ###########################################################
###############################################################################

if __name__ == "__main__":
    os.system("cls")
    my_utilities.version_increment(__file__, sml=1)
    __run_on_example__ = True
    answer = main(parse_input("input.txt"))
    my_utilities.version_increment(__file__, sml=1)
    my_utilities.solve_me(answer, "a")
