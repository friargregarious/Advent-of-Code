"""
################################################################################
#                                                                              #
#                             ADVENT OF CODE: 2024                             #
#                               Restroom Redoubt                               #
#                     https://adventofcode.com/2024/day/14                     #
#                                                                              #
################################################################################
#                                                                              #
# A SOLVED:   2024-12-14 14:03                                                 #
# SOLVER:     friargregarious (greg.denyes@gmail.com)                          #
# HOME:       https://github.com/friargregarious                               #
#                                                                              #
#                   WRITTEN AND TESTED IN PYTHON VER 3.13.0                    #
#                                                                              #
################################################################################
"""
###############################################################################
# imports, globals and helper functions/classes

import os, argparse, toml, sys, time
import solve_utilities as su

from math import prod
from pathlib import Path

def data(input_text_path:Path=Path("input.txt")):

    MAX_WIDE = 11 if DO_EXAMPLE else 101 # X
    MAX_HIGH = 7 if DO_EXAMPLE else 103  # Y

    MAP = { (x, y):[] for y in range(MAX_HIGH) for x in range(MAX_WIDE) }
    
    # 0,0                              MAX_WIDE // 2, 0                             MAX_WIDE, 0
    # 0,MAX_HIGH // 2                  MAX_WIDE // 2, MAX_HIGH // 2                 MAX_WIDE, MAX_HIGH // 2
    # 0,MAX_HIGH                       MAX_WIDE // 2, MAX_HIGH                      MAX_WIDE, MAX_HIGH
    QUADRANTS = {
        1: { "X": (0, MAX_WIDE // 2), "Y":(0, MAX_HIGH // 2) },
        
        2: { "X": (MAX_WIDE // 2, MAX_WIDE), "Y": (0, MAX_HIGH // 2) },
        
        3: { "X": (0, MAX_WIDE // 2), "Y": (MAX_HIGH // 2, MAX_HIGH) },
        
        4: { "X": (MAX_WIDE // 2, MAX_WIDE), "Y": (MAX_HIGH // 2, MAX_HIGH) }
    }
    
    BOTS = {}
    for i, row in enumerate(input_text_path.read_text(encoding="UTF-8").split("\n")):
        # p=x,y  v=3,-3
        _pos, _vel = row.split(" ")
        BOTS[i] = {
            "start": tuple(map(int, _pos[2:].split(","))),
            "vel":  tuple(map(int, _vel[2:].split(","))) ,
            "current": ()
        }

    print('*'*80, 
          f"BOTS: {len(BOTS)}, MAP: {len(MAP)} -> sent to solve_{"a" if DO_A else "b"}(){'   # EXAMPLE #' if DO_EXAMPLE else ''}.".center(80),
          '*'*80,
          sep="\n")
    
    return [BOTS, MAP, MAX_WIDE, MAX_HIGH, QUADRANTS]


def predict_positions(CARGO:list):
    BOTS, MAP, MAX_WIDE, MAX_HIGH = CARGO

    end_seconds = 100
    for bot in BOTS.values():
        x, y = bot["start"]
        dir_x, dir_y = bot["vel"]
        move_x = dir_x * end_seconds
        move_y = dir_y * end_seconds
        bot["current"] = ( (x + move_x) % MAX_WIDE, (y + move_y) % MAX_HIGH )
        
        MAP[bot["current"]].append(bot)


    for y in range(MAX_HIGH):
        for x in range(MAX_WIDE):
            if y == MAX_HIGH//2 or x == MAX_WIDE//2:
                print(" ", end="")
            elif MAP[(x, y)]:
                print(len(MAP[(x, y)]), end="")
            else:
                print(".", end="")

        print()
    print()
    return MAP


###############################################################################
# PART A
###############################################################################
def solve_a(CARGO:list)->int:
    """for solving Part A"""
    print(" Part A ".center(80, "#"))
    BOTS, MAP, MAX_WIDE, MAX_HIGH, QUADRANTS = CARGO
    
    final_positions:dict = predict_positions( [BOTS, MAP, MAX_WIDE, MAX_HIGH] )

    counts = {i:[] for i in QUADRANTS}
    for quad, ranges in QUADRANTS.items():
        for x in range(*ranges["X"]):
            for y in range(*ranges["Y"]):
                if y == MAX_HIGH//2 or x == MAX_WIDE//2:
                    continue
                counts[quad].append(len(final_positions[(x, y)]))
        print(f"quad {quad}: {sum(counts[quad])}")


    quad_sums = [sum(counts[i]) for i in counts if sum(counts[i]) > 0]
    final = prod(quad_sums)

    print(f"final: {final}")

    return final  #prod(counts.values())


###############################################################################
# PART B
###############################################################################

def animate_positions(CARGO:list):
    BOTS, _, MAX_WIDE, MAX_HIGH = CARGO

    target_folder = Path(".output")
    target_folder.mkdir(exist_ok=True)


    end_seconds = 0
    looking = True

    # for end_seconds in range(100):
    while looking:
        end_seconds += 1
        MAP = { (x, y):[] for y in range(MAX_HIGH) for x in range(MAX_WIDE) }
        # if not to_file:
        #     os.system("cls")


        for bot in BOTS.values():
            x, y = bot["start"]
            dir_x, dir_y = bot["vel"]
            move_x = dir_x * end_seconds
            move_y = dir_y * end_seconds
            bot["current"] = ( (x + move_x) % MAX_WIDE, (y + move_y) % MAX_HIGH )
            
            MAP[bot["current"]].append(bot)

        # row = ""

        for y in range(MAX_HIGH):
            row = ""
            for x in range(MAX_WIDE):
                # if y == MAX_HIGH//2 or x == MAX_WIDE//2:
                #     print(" ", end="")
                if MAP[(x, y)]:
                    row += "X"
                else:
                    row += " "
            
            # print(row)
         
            if "XXXXXXXXXX" in row:
                return end_seconds

        # _ = input("Press Enter to continue...")


def solve_b(CARGO:list)->int:
    """for solving Part B"""
    print(" Part B ".center(80, "#"))
    BOTS, MAP, MAX_WIDE, MAX_HIGH, QUADRANTS = CARGO
    
    
    # BOTS, MAP, MAX_WIDE, MAX_HIGH = CARGO

    return animate_positions([BOTS, MAP, MAX_WIDE, MAX_HIGH])


###############################################################################
# command line interface
###############################################################################
if __name__ == "__main__":
    os.system('cls')
    
    # Collect command line arguments
    arguments = argparse.ArgumentParser()
    arguments.add_argument("-e", "--example", help="Bool Flag: Test code with example input instead of default 'input.txt'.", default=False, action="store_true")
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
        source_input = data( Path("example_a.txt") ) if DO_EXAMPLE else data( Path("input.txt") )
        result = solve_a(source_input) if DO_A else solve_b(source_input)

        correct_msg = ""
        match f"{'EXPL' if DO_EXAMPLE else 'REAL'}, {p}":
            case "EXPL, A": correct_answer = 12
            # case "EXPL, A": correct_answer = puzzle.examples[0].answer_a
            case "EXPL, B": correct_answer = puzzle.examples[0].answer_b
            # case "EXPL, B": correct_answer = '34' # puzzle file is corrupt.
            case "REAL, A": correct_answer = puzzle.answer_a if puzzle.answered_a else "unknown"
            case "REAL, B": correct_answer = puzzle.answer_b if puzzle.answered_b else "unknown"
            case _: correct_answer = "unknown"
        
        compare = correct_answer == str(result)
        correct_msg = f"IS CORRECT!! ({correct_answer})" if compare else f"IS NOT CORRECT ({correct_answer})"

        print( f"Solution ({p}): {result} {correct_msg} {f_ex}" )
        if not DO_EXAMPLE: su.submit_result(puzzle, result, p, config)
