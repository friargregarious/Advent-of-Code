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

import math

# from datetime import datetime
from termcolor import colored

# import aocd

###############################################################################
# DECLARATIONS ################################################################
###############################################################################

__version__ = "0.0.52"
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

    assert 0 <= address_value <= 255

    # msg = f"HASH GOT {colored(lens_phrase,'blue')} AND "
    # msg += f"GAVE ME {colored(address_value,'red')}"
    # print(msg)
    return address_value


def hashmap(data_list):
    # parse each phrase
    # baxes are 0 to 255
    boxes = {x: {} for x in range(256)}
    # letters are label of lens
    for inst in data_list:
        # next is operation to perform
        if "=" in inst:
            # it will be followed by a number indicating the focal length of
            # the lens that needs to go into the relevant box
            lens_lable, focal_len = inst.split("=")
            address = address_hash(lens_lable)

            # if lens_lable in boxes[address]:
            boxes[address].update({lens_lable: int(focal_len)})
            # boxes[address][lens_lable] = int(focal_len)

        if inst.endswith("-"):
            # If the operation character is a dash (-),
            # go to the relevant box and remove the lens with the given label
            lens_lable = inst.strip("-")
            address = address_hash(lens_lable)

            if lens_lable in boxes[address].copy():
                boxes[address].pop(lens_lable)

        # box_msg = f"{inst}".rjust(8) + f"{address}".rjust(4)
        # box_msg += f" = Box {colored(address, 'blue')}:"

        # print(box_msg, end=" ")
        # for lens, focus in boxes[address].copy().items():
        #     print(colored(f"[{lens} {focus}]", "green"), end=" ")

        # print()
    return boxes


###############################################################################
# SOLVE PART B ################################################################
###############################################################################


def solve_b(data):
    """For solving PART b of day 15's puzzle.
    the Holiday ASCII String Helper Manual Arrangement Procedure
    or HASHMAP
    """
    refresh()

    focus_boxes = hashmap(data)

    box_results = []

    for box, contents in focus_boxes.items():
        print()
        this_box_result = []
        box_msg = f"Box {colored(box, 'blue')}:"

        print(box_msg, end=" ")
        slot = 0
        for  lens, focus in contents.items():
            slot += 1
            print(colored(f"[{lens} {focus}]", "green"), end=" ")
            
            box_results.append([box + 1, slot, focus])

    # still have to do the multiplication on the final values

    # At the end of the above example,
    # the focusing power of each lens is as follows:

    # rn: 1 (box 0) * 1 (first slot) * 1 (focal length) = 1
    # cm: 1 (box 0) * 2 (second slot) * 2 (focal length) = 4 (5)
    # ot: 4 (box 3) * 1 (first slot) * 7 (focal length) = 28 (33)
    # ab: 4 (box 3) * 2 (second slot) * 5 (focal length) = 40 (73)
    # pc: 4 (box 3) * 3 (third slot) * 6 (focal length) = 72 (145)
    # answer = 145

    solution = sum([math.prod(row) for row in box_results])

    if __run_on_example__:
        print("\n\n")
        for row in box_results:
            print(row, math.prod(row))
            print(f"Final Answer: {solution:,} = {__example_answer__} : {solution==__example_answer__}")

    return solution


###############################################################################
# MAIN ENTRY POINT FOR SUBMITTING AND BENCHMARKING ############################
###############################################################################


def main(source):
    """Main entry point"""
    if __run_on_example__:
        return solve_b(parse_input("example.txt"))

    # print("Correct answer? -> ", solution == __example_answer__)

    return solve_b(parse_input(source))


###############################################################################
# RUNNING_FROM_HOME ###########################################################
###############################################################################

if __name__ == "__main__":
    os.system("cls")
    my_utilities.version_increment(__file__, sml=1)
    # __run_on_example__ = True

    answer = main("inputs.txt")
    my_utilities.version_increment(__file__, sml=1)
    if not __run_on_example__:
        my_utilities.solve_b(answer)