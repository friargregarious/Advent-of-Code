"""
################################################################################
#                                                                              #
#                             ADVENT OF CODE: 2021                             #
#                             Alchemical Reduction                             #
#                     https://adventofcode.com/2021/day/6                      #
#                                                                              #
################################################################################
#                                                                              #
# A SOLVED:   2021-12-07 00:00                                                 #
# SOLVER:     friargregarious (greg.denyes@gmail.com)                          #
# HOME:       https://github.com/friargregarious                               #
#                                                                              #
#                   WRITTEN AND TESTED IN PYTHON VER 3.13.0                    #
#                                                                              #
################################################################################
"""
###############################################################################
# imports, globals and helper functions/classes

import os, argparse, toml, sys
import solve_utilities as su
from pathlib import Path

def data(input_text_path:Path=Path("input.txt")):
    
    temp =  list(map(int, input_text_path.read_text(encoding="UTF-8").split(",")))
    pool =  [temp.count(i) for i in range(9)]
    
    return pool


###############################################################################
# PART A
###############################################################################
def solve_a(pool:list):
    """for solving Part A"""

    days = 18 if DO_EXAMPLE else 80

    print(f" Initial State: {sum(pool):3}".ljust(30), ', '.join([f"{x:5}" for x in pool]))
    for x in range(days):
        zeros = pool.pop(0)
        pool[6] += zeros
        pool.append(zeros)

        print(f"After {x+1:3} days: {sum(pool):7,}".ljust(30), ', '.join([f"{x:5}" for x in pool]))
        
    total = sum(pool)
    return total


###############################################################################
# PART B
###############################################################################
def solve_b(pool):
    """for solving Part B"""
    print(" Part A ".center(80, "#"))
    days = 256

    print(f" Initial State: {sum(pool):3}".ljust(30), ', '.join([f"{x:5}" for x in pool]))
    for x in range(days):
        zeros = pool.pop(0)
        pool[6] += zeros
        pool.append(zeros)

        print(f"After {x+1:3} days: {sum(pool):7,}".ljust(30), ', '.join([f"{x:5}" for x in pool]))
        
    total = sum(pool)
    return total


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
