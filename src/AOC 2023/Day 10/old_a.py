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
from my_utilities import Loc  # , Bouey, version_increment

os.system("cls")
###############################################################################
# DECLARATIONS ################################################################
###############################################################################

__version__ = "0.0.0"
__example_answer__ = 4
__run_on_example__ = True

# looking north,    I must find a | or 7 or F
# looking south,    I must find a | or L or J
# looking west,     I must find a - or L or F
# looking east,     I must find a - or 7 or J

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


class MyGrid(list):
    _current_location: Loc
    start_loc: Loc

    def __init_subclass__(self, values) -> None:
        """this object feeds on lists of lists and
        stores them inside as Loc objects."""
        super().__init_subclass__(values)

        for r_index, row in enumerate(values):
            for c_index, grid_char in enumerate(row):
                cell_loc = Loc(r_index, c_index, grid_char)
                # if grid_char == ".":
                #     self["solid"].append(cell_loc)
                if grid_char == "S":
                    self.start_loc = cell_loc
                else:
                    self.append(cell_loc)

    @property
    def get_sym(self, loc: Loc) -> str:
        return loc.cargo

    def look(self, there: str) -> str:
        """returns the symbol at 'there' direction,
        relative to current location"""

        return self[self + there].cargo

    @property
    def around_me(self, loc):
        my_row, my_col
        possible = []


def take_path(starting_point, current_symbol):
    path_taken = [starting_point]
    possible_directions = []

    if current_symbol in []:
        pass

    go_north = ((-1, 0),)  # looking north
    go_east = ((0, +1),)  # looking east
    go_south = ((+1, 0),)  # looking south
    go_west = ((-1, 0),)  # looking west


START = chr(ord("S"))


def parse_input(source: str = "input.txt") -> list:
    """For parsing source string into usable content"""
    grid = []
    for row in open(source).read().splitlines():
        grid.append(list(row.strip()))

    return grid


def pull_relevant(grid):
    for row in grid:
        for col in row:
            if col == "S":
                pass


###############################################################################
# SOLVE PART A ################################################################
###############################################################################


def solve_a(data):
    """For solving PART a of day 10's puzzle."""
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
    utils.version_increment(__file__, sml=1)


if __run_on_example__:
    answer = main(parse_input("example.txt"), __example_answer__)
else:
    answer = main(parse_input("input.txt"))
    utils.version_increment(__file__, sml=1)
    utils.solve_me(answer, "a")
