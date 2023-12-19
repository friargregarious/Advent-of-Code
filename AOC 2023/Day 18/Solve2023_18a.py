###############################################################################
#              ADVENT OF CODE | 2023 | LAVADUCT LAGOON | PART [A]             #
#                         adventofcode.com/2023/day/18                        #
# SOLVER: --------------------------------------------------- friargregarious #
# CONTACT: --------------------------------------- friar.gregarious@gmail.com #
# HOME: -------------------------------------------------------------- github #
# SOURCE: ---------------------------------- ~/Advent-of-Code/AOC 2023/Day 18 #
# WRITTEN AND TESTED IN: --------------------------------------------- 3.11.6 #
###############################################################################
# IMPORTS #####################################################################
###############################################################################

from dis import Instruction
import os
from re import L
from turtle import pos
import colr

#  from my_utilities import MyConfigParser as MyCfg
# import my_utilities

# import math
# from datetime import datetime
# from termcolor import colored
# import aocd

###############################################################################
# DECLARATIONS ################################################################
###############################################################################

__version__ = "0.0.0"
__example_answer__ = 62
__run_on_example__ = False

###############################################################################
# GATHER_TOOLS ################################################################
###############################################################################


def parse_input(source: str = "input.txt") -> list:
    """For parsing source string into usable content"""
    if source.endswith(".txt"):
        source = open(source).read()
    source = source.split("\n")

    instructions = []
    for row in source:
        direction, distance, colour = row.split(" ")
        instructions.append((direction.strip(), int(distance), colour.strip("()")))
    return instructions


###############################################################################
# SOLVE PART A ################################################################
###############################################################################


def recenter(grid):
    farthest_left = 0
    farthest_up = 0
    for cell in grid:
        y, x = cell[0]
        if y < farthest_up:
            farthest_up = y
        if x < farthest_left:
            farthest_left = x

    if farthest_left < 0:
        farthest_left *= -1
    if farthest_up < 0:
        farthest_up *= -1

    new_grid = []
    for cell in grid:
        loc, clr = cell
        y, x = loc

        new_loc = (farthest_up + y, farthest_left + x)

        new_grid.append((new_loc, clr))

    return new_grid


def go_up(pos, dist):
    y, x = pos
    for _ in range(dist):
        y -= 1
        yield (y, x)


def go_down(pos, dist):
    y, x = pos
    for _ in range(dist):
        y += 1

        yield (y, x)


def go_left(pos, dist):
    y, x = pos
    for _ in range(dist):
        x -= 1

        yield (y, x)


def go_right(pos, dist):
    y, x = pos
    for _ in range(dist):
        x += 1

        yield (y, x)




def solve_a(data):
    """For solving PART a of day 18's puzzle."""
    # ((y,x), "colour")
    grid = set()
    address = (0, 0)

    for inst in data:
        direction, distance, colour = inst
        match direction:
            case "U":
                new_work = [(loc, colour) for loc in go_up(address, distance)]
                
                
                
        address = new_work[-1][0]
        grid.update(new_work)

    grid = recenter(grid)
    solution = len(grid)

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
    for row in parse_input("example.txt"):
        print(row)

    # os.system("cls")
    # my_utilities.version_increment(__file__, sml=1)
    # __run_on_example__ = True

    # answer = main("input.txt")
    # my_utilities.version_increment(__file__, sml=1)
    # my_utilities.solve_me(answer, "a")
