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
    farthest_up, farthest_left = minimums(grid)
    farthest_left *= -1
    farthest_up *= -1

    new_grid = []
    for cell in grid:
        loc, clr = cell
        y, x = loc

        new_loc = (farthest_up + y, farthest_left + x)

        new_grid.append((new_loc, clr))

    return new_grid


def trench_up(pos, dist):
    y, x = pos
    for _ in range(dist):
        y -= 1
        yield (y, x)


def trench_down(pos, dist):
    y, x = pos
    for _ in range(dist):
        y += 1

        yield (y, x)


def trench_left(pos, dist):
    y, x = pos
    for _ in range(dist):
        x -= 1

        yield (y, x)


def trench_right(pos, dist):
    y, x = pos
    for _ in range(dist):
        x += 1

        yield (y, x)


def maximums(grid):
    farthest_right = 0
    farthest_down = 0
    for cell in grid:
        # print("From maxes:", cell)
        loc, _ = cell
        y, x = loc
        if y > farthest_down:
            farthest_down = y
        if x > farthest_right:
            farthest_right = x

    return (farthest_down, farthest_right)


def minimums(grid):
    farthest_left = 0
    farthest_up = 0
    for cell in grid:
        # print("From maxes:", cell)
        loc, _ = cell
        y, x = loc
        if y < farthest_up:
            farthest_up = y
        if x < farthest_left:
            farthest_left = x

    return (farthest_up, farthest_left)


def map_trenches(data):
    grid = set()
    address = (0, 0)

    for inst in data:
        direction, distance, colour = inst
        match direction:
            case "U":
                new_work = [(loc, colour) for loc in trench_up(address, distance)]

            case "D":
                new_work = [(loc, colour) for loc in trench_down(address, distance)]

            case "L":
                new_work = [(loc, colour) for loc in trench_left(address, distance)]

            case "R":
                new_work = [(loc, colour) for loc in trench_right(address, distance)]

        address = new_work[-1][0]
        grid.update(new_work)
    return set(sorted(grid))


def solve_a(data):
    """For solving PART a of day 18's puzzle."""
    grid = map_trenches(parse_input(data))
    grid = recenter(grid)

    deep, wide = maximums(grid)
    grid_dict = {}
    for left, right in grid:
        grid_dict[left] = right

    grid_dict = dict(sorted(grid_dict.items()))

    for row in range(deep + 1):
        for col in range(wide + 1):
            if (row, col) in grid_dict:
                print("#", end="")
            else:
                print(" ", end="")
        print()


    return 0


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
    # for row in parse_input("example.txt"):
    main("example.txt")

    # os.system("cls")
    # my_utilities.version_increment(__file__, sml=1)
    # __run_on_example__ = True

    # answer = main("input.txt")
    # my_utilities.version_increment(__file__, sml=1)
    # my_utilities.solve_me(answer, "a")
