"""
################################################################################
#                                                                              #
#                         ADVENT OF CODE: 2024 DAY 16                          #
#                                Reindeer Maze                                 #
#                     https://adventofcode.com/2024/day/16                     #
#                                                                              #
################################################################################
#                                                                              #
# A SOLVED:   N/A                                                              #
# B SOLVED:   N/A                                                              #
# SOLVER:     friargregarious (greg.denyes@gmail.com)                          #
# HOME:       https://github.com/friargregarious                               #
#                                                                              #
#                   WRITTEN AND TESTED IN PYTHON VER 3.13.7                    #
#                                                                              #
################################################################################
"""

###############################################################################
# imports, globals and helper functions/classes

import os, argparse, toml, sys
import solve_utilities as su
from pathlib import Path
from uuid import uuid4


def data(input_text_path: Path = Path("input.txt")) -> list[str]:
    """
    Reads in a file at the given path, and returns a list of strings, one for each line in the file.

    :param input_text_path: A Path object pointing to a file to read in.
    :return: A list of strings, one for each line in the file.
    """
    text_source_list = input_text_path.read_text(encoding="UTF-8").split("\n")

    return text_source_list


class GameMap:
    def __init__(self, text_source_list):
        """
        Initializes a GameMap object with a list of strings representing a map.

        The map is iterated over, and any '#' characters are added to the walls list,
        any '.' characters are added to the paths list, any 'S' characters are added to
        the start attribute, and any 'E' characters are added to the end attribute.

        :param text_source_list: A list of strings representing a map.
        :return: None
        """
        self.walls = []
        self.paths = []
        for row in text_source_list:
            for col in row:
                if col == "#":
                    self.walls.append((row, col))
                elif col == ".":
                    self.paths.append((row, col))
                elif col == "S":
                    self.start = (row, col)
                elif col == "E":
                    self.end = (row, col)

NORTH = 1
EAST = 2
SOUTH = 3
WEST = 4

class Deer:
    def __init__(self, start_tile: tuple[int, int]):
        """
        Initializes a Deer object with name and score.

        :param name: The name of the deer.
        :param score: The score of the deer.
        :return: None
        """
        self.name = uuid4().hex
        self.score = 0
        self.facing = EAST
        self.row, self.col = start_tile
        self._log = []

    def log(self, message):
        self._log.append(message)
    
    @property
    def pos(self) -> tuple[int, int]:
        """
        Return the position of the deer as a tuple of (row, col).

        :return: tuple[int, int]
        """
        return (self.row, self.col)

def move_forward(deer, raceMap):
    """
    Move the deer forward one step in the direction it is facing.
    
    They can move forward one tile at a time (increasing their score by `1` point), but never into a wall (`#`).

    If the deer is facing NORTH, it moves one row up.
    If the deer is facing EAST, it moves one column right.
    If the deer is facing SOUTH, it moves one row down.
    If the deer is facing WEST, it moves one column left.
    """
    if deer.facing == NORTH:
        deer.row -= 1
    elif deer.facing == EAST:
        deer.col += 1
    elif deer.facing == SOUTH:
        deer.row += 1
    elif deer.facing == WEST:
        deer.col -= 1

    _old = deer.score
    deer.score += 1
    deer.log(f"Moved {deer.facing} to {deer.pos} score: {_old} -> {deer.score}")

    if deer.pos == raceMap.end:
        return deer

def turn_left(deer):
    """
    Turns the deer 90 degrees to the left.

    They can also rotate clockwise or counterclockwise 90 degrees at a time (increasing their score by `1000` points).

    :param deer: The deer object to turn.
    :return: None
    """
    deer.facing = (deer.facing - 1) % 4

    _old = deer.score
    deer.score += 1000    
    deer.log(f"Turned LEFT, now facing {deer.facing} @ {deer.pos} score: {_old} -> {deer.score}")

def turn_right(deer):
    """
    Turns the deer 90 degrees to the right.

    They can also rotate clockwise or counterclockwise 90 degrees at a time (increasing their score by `1000` points).

    :param deer: The deer object to turn.
    :return: None
    """
    deer.facing = (deer.facing + 1) % 4
    deer.log(f"Turned RIGHT, now facing {deer.facing} @ {deer.pos}")

def look_ahead(deer, raceMap):
    if deer.facing == NORTH:
        ahead = deer.row - 1, deer.col
    elif deer.facing == EAST:
        ahead = deer.row, deer.col + 1
    elif deer.facing == SOUTH:
        ahead = deer.row + 1, deer.col
    elif deer.facing == WEST:
        ahead = deer.row, deer.col - 1

    if ahead in raceMap.walls:
        return "WALL"
    elif ahead in raceMap.paths:
        return "PATH"
    else:
        return "END"

def spawn_deer(herd, thisDeer, raceMap):
    # one new deer at start
    x = Deer(raceMap.start)
    
    # one new deer goes LEFT
    n = Deer(thisDeer.pos)
    n.facing = thisDeer.facing
    n.score = thisDeer.score
    n._log = thisDeer._log
    turn_left(n)
    
    # this deer goes RIGHT
    turn_right(thisDeer)

    # put them all back into the herd
    herd[n.name] = n
    herd[x.name] = x
    herd[thisDeer.name] = thisDeer

    # drop the slowest deer to maintain a fast herd
    # and to prevent memory issues
    cutoff = sorted([w.score for w in herd.values()], reverse=False)[100]

    for name, deer in herd.items():
        if deer.score <= cutoff:
            del herd[name]
        


###############################################################################
# PART A
###############################################################################
def solve_a(source):
    """for solving Part A"""
    print("Part A") if VERBOSE else None

    gameMap = GameMap(source)

    herd = {}






###############################################################################
# PART B
###############################################################################
def solve_b(source):
     """for solving Part B"""

    print("Part B") if VERBOSE else None

    return 0


###############################################################################
# command line interface
###############################################################################
if __name__ == "__main__":
    os.system("cls")

    # Collect command line arguments
    arguments = argparse.ArgumentParser()
    for arp, ark in su.ARGS_LIST:
        arguments.add_argument(*arp, **ark)
    args = arguments.parse_args()

    su.print_args(vars(args))

    # Load puzzle parameters
    config = toml.load(Path(".env"))

    DO_A, DO_B = not args.part_b, args.part_b
    DO_EXAMPLE = args.example
    VERBOSE = args.verbose

    # open puzzle info
    puzzle = su.open_puzzle(config)

    if args.discord:
        su.Discord(puzzle=puzzle, config=config)
        sys.exit()

    if args.refresh:
        su.refresh_readme(puzzle)
        sys.exit()

    if args.submit:
        p = "A" if DO_A else "B"

        f_ex = "(From Example)" if DO_EXAMPLE else "(From input)"
        source_input = (
            data(Path("example_a.txt")) if DO_EXAMPLE else data(Path("input.txt"))
        )
        result = solve_a(source_input) if DO_A else solve_b(source_input)

        correct_msg = ""
        match f"{'EXPL' if DO_EXAMPLE else 'REAL'}, {p}":
            case "EXPL, A":
                correct_answer = puzzle.examples[0].answer_a
            # case "EXPL, B": correct_answer = puzzle.examples[0].answer_b
            case "EXPL, B":
                correct_answer = "34"  # puzzle file is corrupt.
            case "REAL, A":
                correct_answer = puzzle.answer_a if puzzle.answered_a else "unknown"
            case "REAL, B":
                correct_answer = puzzle.answer_b if puzzle.answered_b else "unknown"
            case _:
                correct_answer = "unknown"

        compare = correct_answer == str(result)
        correct_msg = (
            f"IS CORRECT!! ({correct_answer})"
            if compare
            else f"IS NOT CORRECT ({correct_answer})"
        )

        print(f"Solution ({p}): {result} {correct_msg} {f_ex}")
        if not DO_EXAMPLE:
            su.submit_result(puzzle, result, p, config)
