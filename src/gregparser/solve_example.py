"""
{#HEADER}
"""
###############################################################################
# imports, globals and helper functions/classes

import os, argparse, toml
import solve_utilities as su
from time import sleep
from markdownify import markdownify
from pathlib import Path

def data(input_text_path:Path=Path("input.txt")):

    text_source_list = input_text_path.read_text(encoding="UTF-8").split("\n")

    return text_source_list





###############################################################################
# PART A
###############################################################################
def solve_a(source):
    """for solving Part A"""

    return 0


###############################################################################
# PART B
###############################################################################
def solve_b(source):
    """for solving Part B"""

    return 0


###############################################################################
# command line interface
###############################################################################
if __name__ == "__main__":
    os.system('cls')
    
    # Collect command line arguments
    arg = argparse.ArgumentParser()
    arg.add_argument("-e", "--example", help="Bool Flag: Test code with example input instead of default 'input.txt'.", default=False, action="store_true")
    arg.add_argument("-s", "--submit", help="Bool Flag: Submit answer to server. (defaults to False).", default=False, action="store_true")
    arg.add_argument("-b", "--part_b", help="Bool Flag: Choses parts 'A' or 'B' to run. (defaults to 'A').", default=False, action="store_true")
    arg.add_argument("-r", "--refresh", help="Bool Flag: Refresh/update the readme.md file and exit.", default=False, action="store_true")
    arg.add_argument("-d", "--discord", help="Bool Flag: Send message to discord channel and exit.", default=False, action="store_true")
    args = arg.parse_args()
    
    su.print_args(vars(args))

    # Load puzzle parameters
    config = toml.load(Path('.env'))
    _puzzle_path = config['puzzle']['path']
    
    DO_A = not args.part_b
    DO_B = args.part_b
    DO_EXAMPLE = args.example
    SUBMIT_PUZZLE = args.submit
    REFRESH = args.refresh
    DISCORD = args.discord
    
    # open puzzle info
    puzzle = su.open_puzzle(config)
    
    if REFRESH:
        su.refresh_readme(puzzle)

    # Setup input data
    if DO_EXAMPLE and DO_A:
        result = solve_a(data(Path("example_a.txt")))
    elif DO_EXAMPLE and DO_B:
        result = solve_b(data(Path("example_b.txt")))
    else:
        source_input = data(Path("input.txt"))
        if DO_A:
            result = solve_a(source_input)
        else:
            result = solve_b(source_input)

    if SUBMIT_PUZZLE:
        p = "A" if DO_A else "B"
        su.submit_result(puzzle, result, p, _puzzle_path)
