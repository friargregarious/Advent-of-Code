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
__example_answer__ = 1514
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
    """For solving PART a of day 4's puzzle."""
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
