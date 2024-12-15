"""
################################################################################
#                                                                              #
#                             ADVENT OF CODE: 2024                             #
#                                Warehouse Woes                                #
#                     https://adventofcode.com/2024/day/15                     #
#                                                                              #
################################################################################
#                                                                              #
# A SOLVED:   2024-12-15 09:18                                                 #
# SOLVER:     friargregarious (greg.denyes@gmail.com)                          #
# HOME:       https://github.com/friargregarious                               #
#                                                                              #
#                  WRITTEN AND TESTED IN PYTHON VER 3.13.0                   #
#                                                                              #
################################################################################
"""
###############################################################################
# imports, globals and helper functions/classes

import os, argparse, toml, sys
import solve_utilities as su
from pathlib import Path


def data(input_text_path:Path=Path("input.txt")):

    # MAP = {}
    DIRS = ""
    ROBOT = (0, 0)
    BOXES = []
    WALLS = []

    map_part, dirs_part = input_text_path.read_text(encoding="UTF-8").split("\n\n")
    MAX_R = len(map_part.split("\n"))
    MAX_C = len(map_part.split("\n")[0])
    
    for r, row in enumerate(map_part.split("\n")):
        for c, item in enumerate(row):
            if item == "#":     WALLS.append( (r, c) )
            elif item == "O":   BOXES.append( (r, c) )
            elif item == "@":   ROBOT = (r, c)
    
    cardinal = {"^": "N", ">": "E", "v": "S", "<": "W"}
    DIRS =  "".join([cardinal[c] for c in dirs_part.replace("\n", "")])

    return [DIRS, ROBOT, WALLS, BOXES, MAX_R, MAX_C]


def next_step(location, dir):
    r, c = location

    if dir == "N":   return  (  r-1,     c        )
    elif dir == "S": return  (  r+1,     c        )
    elif dir == "W": return  (  r,       c - 1    )
    elif dir == "E": return  (  r,       c + 1    )


###############################################################################
# PART A
###############################################################################

def BLOCKED(location, WALLS):
    return (location) in WALLS

def BOXED(location, BOXES):
    return (location) in BOXES

def draw_map(ROBOT, BOXES, WALLS, MAX_R, MAX_C):
    for r in range(MAX_R):
        for c in range(MAX_C):
            if (r, c) == ROBOT:     print("@", end="")
            elif (r, c) in BOXES:   print("O", end="")
            elif (r, c) in WALLS:   print("#", end="")
            else:                   print(".", end="")
        print()



def solve_a(cargo):
    """for solving Part A"""
    print(" Part A ".center(80, "#"))
    
    DIRS, ROBOT, WALLS, BOXES, MAX_R, MAX_C = cargo
    GPS = 0
    for move in DIRS:
        step = next_step(ROBOT, move)

        if BLOCKED(step, WALLS):
            print(f"\n{move} {ROBOT} -> {step} robot blocked by wall")            
            draw_map(ROBOT, BOXES, WALLS, MAX_R, MAX_C) if DO_EXAMPLE else None
            continue

        if not BLOCKED(step, WALLS) and not BOXED(step, BOXES):
            print(f"\n{move} {ROBOT} -> {step}")
            ROBOT = step
            draw_map(ROBOT, BOXES, WALLS, MAX_R, MAX_C) if DO_EXAMPLE else None
            continue

        if BOXED(step, BOXES):
            affected_boxes = [step]
            while next_step(affected_boxes[-1], move) in BOXES:
                affected_boxes.append(next_step(affected_boxes[-1], move))

            if next_step(affected_boxes[-1], move) in WALLS:
                print(f"\n{move} {ROBOT} -> {step} box blocked by wall")
                draw_map(ROBOT, BOXES, WALLS, MAX_R, MAX_C) if DO_EXAMPLE else None
                continue

            # i = BOXES.index()
            # print(BOXES)
            
            print("**", BOXES) if DO_EXAMPLE else None
            BOXES.remove(step)
            print("**", BOXES) if DO_EXAMPLE else None
            BOXES.append(next_step(affected_boxes[-1], move))
            print("**", BOXES) if DO_EXAMPLE else None
            
            print(f"\n{move} {ROBOT} -> {step} pushed {len(affected_boxes)} box{'es' if len(affected_boxes) > 1 else ''}")
            ROBOT = step
            draw_map(ROBOT, BOXES, WALLS, MAX_R, MAX_C) if DO_EXAMPLE else None


    GPS = calc_safety(BOXES)

    return GPS


def calc_safety(BOXES):
    # The GPS coordinate of a box is equal to 100 times its distance from the 
    # top edge of the map plus its distance from the left edge of the map. 
    # (This process does not stop at wall tiles; measure all the way to the edges of the map.)
    safe = 0
    for r, c in BOXES:
        safe += 100 * r + c
    return safe

###############################################################################
# PART B
###############################################################################
def solve_b(cargo):
    """for solving Part B"""

    print(" Part B ".center(80, "#"))
    DIRS, ROBOT, WALLS, BOXES = cargo
    

    GPS = 0
    return GPS


###############################################################################
# command line interface
###############################################################################
if __name__ == "__main__":
    os.system('cls')
    
    # Collect command line arguments
    arguments = argparse.ArgumentParser()
    arguments.add_argument("-e", "--example", help="Bool Flag: Test code with example input instead of default 'input.txt'.", default=False, action="store_true")
    arguments.add_argument("-e2", "--example2", help="Bool Flag: Test code with example2 input instead of default 'input.txt'.", default=False, action="store_true")
    arguments.add_argument("-s", "--submit", help="Bool Flag: Submit answer to server. (defaults to False).", default=False, action="store_true")
    arguments.add_argument("-b", "--part_b", help="Bool Flag: Choses parts 'A' or 'B' to run. (defaults to 'A').", default=False, action="store_true")
    arguments.add_argument("-r", "--refresh", help="Bool Flag: Refresh/update the readme.md file and exit.", default=False, action="store_true")
    arguments.add_argument("-d", "--discord", help="Bool Flag: Send message to discord channel and exit.", default=False, action="store_true")
    arguments.add_argument("-v", "--verbose", help="Bool Flag: allow in code print statements.", default=False, action="store_true")
    
    args = arguments.parse_args()

    su.print_args(vars(args))

    # Load puzzle parameters
    config = toml.load(Path('.env'))
    
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

        f_ex = '(From Example)' if DO_EXAMPLE else '(From input)'
        source_input = data( Path("example_a.txt") ) if DO_EXAMPLE else data( Path("input.txt") ) if not args.example2 else data( Path("example_b.txt") )
        
        result = solve_a(source_input) if DO_A else solve_b(source_input)

        correct_msg = ""
        match f"{'EXPL' if DO_EXAMPLE else 'REAL'}, {p}":
            case "EXPL, A": correct_answer = puzzle.examples[0].answer_a
            case "EXPL, B": correct_answer = puzzle.examples[0].answer_b
            # case "EXPL, B": correct_answer = '34' # puzzle file is corrupt.
            case "REAL, A": correct_answer = puzzle.answer_a if puzzle.answered_a else "unknown"
            case "REAL, B": correct_answer = puzzle.answer_b if puzzle.answered_b else "unknown"
            case _: correct_answer = "unknown"
        
        compare = correct_answer == str(result)
        correct_msg = f"IS CORRECT!! ({correct_answer})" if compare else f"IS NOT CORRECT ({correct_answer})"

        print( f"Solution ({p}): {result} {correct_msg} {f_ex}" )
        if not DO_EXAMPLE: su.submit_result(puzzle, result, p, config)
