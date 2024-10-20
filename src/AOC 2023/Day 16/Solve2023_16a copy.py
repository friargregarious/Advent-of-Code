""" module doc string """
###############################################################################
#          ADVENT OF CODE | 2023 | THE FLOOR WILL BE LAVA | PART [A]          #
#                         adventofcode.com/2023/day/16                        #
# SOLVER: --------------------------------------------------- friargregarious #
# CONTACT: --------------------------------------- friar.gregarious@gmail.com #
# HOME: -------------------------------------------------------------- github #
# SOURCE: ---------------------------------- ~/Advent-of-Code/AOC 2023/Day 16 #
# WRITTEN AND TESTED IN: --------------------------------------------- 3.11.6 #
###############################################################################
# IMPORTS #####################################################################
###############################################################################

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

__version__ = "0.0.92"
__example_answer__ = 46
__run_on_example__ = False

###############################################################################
# GATHER_TOOLS ################################################################
###############################################################################


def parse_input(source: str = "input.txt") -> list[str,]:
    """For parsing source string into usable content"""
    #  square grid containing
    #       empty space (.),
    #       mirrors (/ and \), and
    #       splitters (| and -).

    if source.endswith(".txt"):
        raw = open(source, "r", encoding="utf-8").read()
        return raw.split("\n")
    return source.split("\n")


class Grid(list):
    """doc string"""

    @property
    def max_col(self):
        """doc string"""
        return len(self[0]) - 1

    @property
    def max_row(self):
        """doc string"""
        return len(self) - 1

    def is_legal(self, mvr: dict) -> bool:
        """is this position a legal location on the grid?"""
        r, c = mvr["c_loc"]
        return (0 <= r <= self.max_row) and (0 <= c <= self.max_col)

    def whats_at(self, mvr: dict) -> int:
        """What symbol is at this location on the grid?"""
        m_row, m_col = mvr["c_loc"]
        string = self[m_row]
        charfound = string[m_col]
        return ord(charfound)


# available directions
NORTH = (-1, 0)
SOUTH = (+1, 0)
EAST = (0, +1)
WEST = (0, -1)


# nice idea but not going to be used in this project
def compass(direction):
    """simple compass"""
    directions = {
        "N": (-1, 0),
        "S": (+1, 0),
        "E": (0, +1),
        "W": (0, -1),
        (-1, 0): "NORTH",
        (+1, 0): "SOUTH",
        (0, +1): "EAST",
        (0, -1): "WEST",
        "NORTH": (-1, 0),
        "SOUTH": (+1, 0),
        "EAST": (0, +1),
        "WEST": (0, -1),
    }
    return directions[direction]


def mover_agent(c_loc: tuple, c_dir: tuple, str: int = 0) -> dict:
    """format for making movers"""
    return {"c_loc": c_loc, "c_dir": c_dir, "str": str}


def is_moving(mvr: dict) -> tuple:
    """Returns the direction this mover moving."""
    return mvr["c_dir"]


# def new_dir(mvr: dict, c_dir: tuple) -> dict:
#     """returns the mover with a new direction"""
#     new_bearing = mvr.copy()
#     new_bearing.update({"c_dir": c_dir})
#     return new_bearing


def move_me(mvr: dict) -> dict:
    """returns the mover after incrementing position
    1 placement as per direction.
    """
    new_pos = mvr.copy()
    r, c = new_pos["c_loc"]
    y, x = new_pos["c_dir"]
    new_pos.update({"c_loc": (r + y, c + x)})
    return new_pos


def hit_124(mvr: dict) -> list:
    """'|' = 124"""
    match compass(is_moving(mvr)):
        case "EAST":
            newlist = [
                mover_agent(mvr["c_loc"], NORTH, mvr["str"] - 1),
                mover_agent(mvr["c_loc"], SOUTH, mvr["str"] - 1),
            ]

        case "WEST":
            newlist = [
                mover_agent(mvr["c_loc"], NORTH, mvr["str"] - 1),
                mover_agent(mvr["c_loc"], SOUTH, mvr["str"] - 1),
            ]
            return newlist

        case _:
            # if is_moving(mvr) == NORTH or is_moving(mvr) == SOUTH:
            newlist = [mvr]
    return newlist


def hit_47(mvr: dict) -> list:
    """
    What happens when I run into '/' = 47
    """
    match compass(is_moving(mvr)):
        case "NORTH":
            # c_dir = EAST
            return [mover_agent(mvr["c_loc"], EAST, mvr["str"] - 1)]
        case "SOUTH":
            # c_dir = WEST
            return [mover_agent(mvr["c_loc"], WEST, mvr["str"] - 1)]
        case "EAST":
            # c_dir = NORTH
            return [mover_agent(mvr["c_loc"], NORTH, mvr["str"] - 1)]
        case "WEST":
            # c_dir = SOUTH
            return [mover_agent(mvr["c_loc"], SOUTH, mvr["str"] - 1)]


def hit_45(mvr):
    """'-' = 45"""
    match compass(is_moving(mvr)):
        case "NORTH":
            new_movers = [
                mover_agent(mvr["c_loc"], EAST, mvr["str"] - 1),
                mover_agent(mvr["c_loc"], WEST, mvr["str"] - 1),
            ]
        case "SOUTH":
            new_movers = [
                mover_agent(mvr["c_loc"], EAST, mvr["str"] - 1),
                mover_agent(mvr["c_loc"], WEST, mvr["str"] - 1),
            ]
        case _:
            new_movers = [mvr]
    return new_movers


def hit_92(mvr):
    """
    '\' = 92
    """
    match compass(is_moving(mvr)):
        case "EAST":  # c_dir = SOUTH
            new_movers = [mover_agent(mvr["c_loc"], SOUTH, mvr["str"] - 1)]

        case "WEST":  # c_dir = NORTH
            new_movers = [mover_agent(mvr["c_loc"], NORTH, mvr["str"] - 1)]

        case "NORTH":  # c_dir = WEST
            new_movers = [mover_agent(mvr["c_loc"], WEST, mvr["str"] - 1)]

        case "SOUTH":  # c_dir = EAST
            new_movers = [mover_agent(mvr["c_loc"], EAST, mvr["str"] - 1)]
    return new_movers


def decide(mvr: dict, grid: Grid) -> list:
    """using mover's current position and bearing,
    we return the new direction of the mover or in
    some cases, add new movers to the queue if there
    is a beam split.

    Dealing with escaped characters, we'll just be
    looking at the character ordinals.
    '.' = 46, '\' = 92, '/' = 47, '|' = 124, '-' = 45
    """
    new_movers: list = []

    match grid.whats_at(mvr):
        case 45:  # '-' = 45
            new_movers = hit_45(mvr)

        case 124:  # '|' = 124
            new_movers = hit_124(mvr)

        case 92:
            new_movers = hit_92(mvr)

        case 47:  # '/' = 47
            new_movers = hit_47(mvr)

        case _:  # 46:  # '.' = 46
            new_movers = [mvr]

    new_positions = []

    # testing that new position is within legal positions
    for this_mvr in new_movers:
        moved = move_me(this_mvr.copy())

        if grid.is_legal(moved) and this_mvr["str"] > 0:
            
            new_positions.append(this_mvr)
        # if not legal, mover_agent collected into bit-bucket.

    return new_positions


def refresh_screen(grid: Grid, energy_set: set, movers_2_move: list) -> None:
    """doc string"""
    os.system("cls")
    print("   Count Energised:".rjust(20), len(energy_set))
    print("Count Active Beams:".rjust(20), len(movers_2_move))

    for y, row in enumerate(grid):
        for x, f_char in enumerate(row):
            if (y, x) in energy_set:
                printme = colored(f_char, "white", "on_light_blue")

            # elif

            else:
                printme = f_char

            # print(printme, end="")
        # print()


###############################################################################
# SOLVE PART A ################################################################
###############################################################################


def solve_a(data):
    """For solving PART a of day 16's puzzle."""
    energized = set()
    movers_to_move = [mover_agent((0, 0), EAST, str=1000)]

    my_grid = Grid(data)

    while len(movers_to_move) > 0:
        # reset the queues of movers before they move
        movers_that_moved = []

        # all movers, after visiting a location, have energized that loc
        for this_mvr in movers_to_move:
            energized.add(this_mvr["c_loc"])

        # now they all reorient their bearings if necessary
        for this_mvr in movers_to_move:
            queue = decide(this_mvr, my_grid)
            movers_that_moved.extend([move_me(m_mvr) for m_mvr in queue])

        # # reset the original queue of movers
        # movers_to_move = []

        # # now we move them all
        # for this_mvr in movers_that_moved:
        #     movers_that_moved.append(move_me(this_mvr))

        movers_to_move = []
        for beam in movers_that_moved:
            if my_grid.is_legal(beam):
                temp = beam
                temp["str"] -= 1
                movers_to_move.append(temp)


        # movers_to_move = movers_that_moved

        refresh_screen(my_grid, energized, movers_to_move)

        # _ = input()

    solution = len(energized)
    if __run_on_example__:
        print(
            f"My solution is {solution} and it matches the example",
            f"answer: {solution == __example_answer__}",
        )

    return solution


###############################################################################
# MAIN ENTRY POINT FOR SUBMITTING AND BENCHMARKING ############################
###############################################################################


def main(source):
    """Main entry point"""
    if __run_on_example__:
        return solve_a(parse_input("example.txt"))

    return solve_a(parse_input(source))


###############################################################################
# RUNNING_FROM_HOME ###########################################################
###############################################################################

if __name__ == "__main__":
    os.system("cls")
    my_utilities.version_increment(__file__, sml=1)

    # __run_on_example__ = True
    ANSWER = main("inputs.txt")