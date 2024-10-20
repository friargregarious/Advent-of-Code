###############################################################################
#                 ADVENT OF CODE | 2023 | PIPE MAZE | PART [A]                #
#                         adventofcode.com/2023/day/10                        #
# SOLVER: -------------------------------------------------- friargregarious #
# CONTACT: -------------------------------------- friar.gregarious@gmail.com #
# HOME: ------------------------------------------------------------- github #
# SOURCE: --------------------------------- ~/Advent-of-Code/AOC 2023/Day 10 #
# WRITTEN AND TESTED IN: -------------------------------------------- 3.11.6 #
###############################################################################
# IMPORTS #####################################################################
###############################################################################

import os
import my_utilities
from my_utilities import Loc  # , Bouey, version_increment

os.system("cls")
###############################################################################
# DECLARATIONS ################################################################
###############################################################################

__version__ = "0.0.1"
__example_answer__ = 4
__run_on_example__ = True

START = chr(ord("S"))

# "|" = "up and down"
# "-": "left and right"
# "L": "up and right"
# "J": "Up and left"
# "7": "down and left"
# "F": "down to right"
# "S" = "start"

# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.

# S is the starting position of the animal; there is a pipe on this tile, but
# your sketch doesn't show what shape the pipe has.

###############################################################################
# GATHER_TOOLS ################################################################
###############################################################################

# so, if you have 2 tuples (1,1) and (2,2) and you add them together,
# you would think that you'd get back (3,3). But you get (1,3,2).
# so I had to sort of recreate the Tuple class obj where it's almost the
# same, but it adds left to left and right to right. also, it carries the
# symbol as useless cargo that doesn't really do anything.

valid_paths = {
    # looking north, valid path means I must find a | or 7 or F
    "NORTH": {Loc(-1, 0): ["|", "7", "F"]},
    # looking south, valid path means I must find a | or L or J
    "SOUTH": {Loc(+1, 0): ["|", "L", "J"]},
    # looking west,  valid path means I must find a - or L or F
    "WEST": {Loc(0, -1): ["-", "L", "F"]},
    # looking east,  valid path means I must find a - or 7 or J
    "EAST": {Loc(0, +1): ["-", "7", "J"]},
}


def find_start(grid):
    for key, value in grid.items():
        if value == START:
            return {key: value}


def look(grid, loc_from: Loc, loc_to: Loc) -> str:
    """returns the symbol at 'there' direction,
    relative to current location"""

    return grid[loc_from + loc_to]


def around_me(grid, loc):
    found = {}
    valid = {}
    for dir in [NORTH, EAST, SOUTH, WEST]:
        found[Loc(loc + dir)] = grid[loc + dir]

    for location, symbol in found.items():  # "."
        if symbol in ["S", "|", "-", "L", "J", "7", "F"]:
            valid.update({location: symbol})
    return valid


# go_north = ((-1, 0),)  # looking north
# go_east = ((0, +1),)  # looking east
# go_south = ((+1, 0),)  # looking south
# go_west = ((-1, 0),)  # looking west


def parse_input(source: str = "input.txt") -> list:
    """For parsing source string into usable content"""
    info = []
    for row in open(source,"r").read().splitlines():
        info.append(list(row.strip()))

    return info


def is_north(me, it):
    pass


def is_south(me, it):
    pass


def is_east(me, it):
    pass


def is_west(me, it):
    pass


default_path = [(1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (3, 2), (3, 1), (2, 1), (1, 1)]


def draw_grid(grid, path_taken=default_path):
    widest = max(grid)
    for row in grid:
        print(row)


###############################################################################
# SOLVE PART A ################################################################
###############################################################################


def solve_a(data):
    """For solving PART a of day 10's puzzle."""
    # 1) make the grid
    work_grid = parse_input(data)
    # 2) find the starting point and put it in my logbook
    path_taken = [find_start(work_grid)]
    draw_grid(work_grid)
    # this part will loop until done

    # 3) set the last position as my current location
    current_loc = path_taken[-1]
    # 4) find valid paths around me
    available = around_me(current_loc)

    for x in available:
        if is_north():
            pass

    solution = 0
    return solution


###############################################################################
# MAIN ENTRY POINT FOR SUBMITTING AND BENCHMARKING ############################
###############################################################################


def main(source, ex_answer=0):
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
    my_utilities.solve_me(answer, "a")
