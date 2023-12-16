###############################################################################
#               ADVENT OF CODE | 2023 | LENS LIBRARY | PART [B]               #
#                         adventofcode.com/2023/day/15                        #
# SOLVER: --------------------------------------------------- friargregarious #
# CONTACT: --------------------------------------- friar.gregarious@gmail.com #
# HOME: -------------------------------------------------------------- github #
# SOURCE: ---------------------------------- ~/Advent-of-Code/AOC 2023/Day 15 #
# WRITTEN AND TESTED IN: --------------------------------------------- 3.11.6 #
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
__example_answer__ = 145
__run_on_example__ = False


###############################################################################
# GATHER_TOOLS ################################################################
###############################################################################
def refresh():
    os.system("cls")


def parse_input(source: str = "inputs.txt") -> list:
    """For parsing source string into usable content"""

    if source.endswith(".txt"):
        return open(source).read().split(",")
    return source.split(",")


def address_hash(lens_phrase):
    address_value = 0

    for char in lens_phrase:
        # step 0: get the ord value of the character
        ch_ord = ord(char)

        # step 1: add the ordinal of the char to our current value
        address_value += ch_ord

        # step 2: multiply our address by 17
        address_value *= 17

        # step 3: return the remainder of address / 256
        address_value %= 256

    return address_value


def hashmap(data_list):
    # parse each phrase
    # baxes are 0 to 255
    boxes = {x: {} for x in range(256)}
    # letters are label of lens
    for inst in data_list:
        refresh()
        # next is operation to perform
        if "=" in inst:
            # it will be followed by a number indicating the focal length of
            # the lens that needs to go into the relevant box
            lens_lable, focal_len = inst.split("=")
            address = hash(lens_lable)

            boxes[address][lens_lable] = int(focal_len)

        if inst.endswith("-"):
            # If the operation character is a dash (-),
            # go to the relevant box and remove the lens with the given label
            lens_lable = inst.strip("-")
            address = hash(lens_lable)

            if lens_lable in boxes[address]:
                boxes[address].pop(lens_lable)

    for box, contents in boxes.items():
        print()
        print(f"Box {box}: ", end="")
        for lens, focus in contents.items():
            print(f"[{lens} {focus}] ")




###############################################################################
# SOLVE PART B ################################################################
###############################################################################


def solve_b(data):
    """For solving PART b of day 15's puzzle.
    the Holiday ASCII String Helper Manual Arrangement Procedure
    or HASHMAP
    """

    return solution


###############################################################################
# MAIN ENTRY POINT FOR SUBMITTING AND BENCHMARKING ############################
###############################################################################


def main(source):
    """Main entry point"""
    if __run_on_example__:
        return solve_b(parse_input("example.txt"))

    print("Correct answer? -> ", solution == __example_answer__)

    return solve_b(parse_input(source))


###############################################################################
# RUNNING_FROM_HOME ###########################################################
###############################################################################

if __name__ == "__main__":
    os.system("cls")
    my_utilities.version_increment("b", sml=1)
    __run_on_example__ = True
    answer = main(parse_input("input.txt"))
    my_utilities.version_increment("a", sml=1)
    my_utilities.solve_me(answer, "b")
