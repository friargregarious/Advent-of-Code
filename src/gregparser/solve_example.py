"""
###############################################################################
#
#                              ADVENT OF CODE: {year}
#                                  {title}
#                      {url}
#
###############################################################################
#
# SOLVER:   friargregarious (greg.denyes@gmail.com)
# SOLVED:   {date_solved}
# HOME:     https://github.com/friargregarious
# SOURCE:   https://github.com/friargregarious/AOC-2023
#
# WRITTEN AND TESTED IN PYTHON VER {version}
#
###############################################################################
"""
###############################################################################
# imports, globals and helper functions/classes

import os, sys, argparse
from pathlib import Path

def data(input_text_path:Path=Path("input.txt")):

    text_source_list = input_text_path.read_text(encoding="UTF-8").split("\n")

    return text_source_list





###############################################################################
# PART A
###############################################################################
def solve_a(source):
    """for solving Part A"""

    solution = source

    return solution


###############################################################################
# PART B
###############################################################################
def solve_b(source):
    """for solving Part B"""

    solution = source
    return solution


###############################################################################
def main(source, do_a=False, do_b=False):
    """ENTRY POINT FOR SUBMITTING & BENCHMARKING"""
    solution_a = solve_a(source=data(source))
    solution_b = solve_b(source=data(source))

    return (solution_a, solution_b)


###############################################################################
# command line interface
if __name__ == "__main__":
    arg = argparse.ArgumentParser()
    arg.add_argument("--example", help="test with example input (defaults to real input)", type=bool, default=False)
    arg.add_argument("--parts", help="chose parts 'A' or 'B' to run. (defaults to both: 'AB')", type=str, default="AB")
    arg.add_argument("--help", help="defaults to parts 'AB' and standard 'input.txt'.", type=str, default="AB")
    
    args = arg.parse_args()
    
    if args.example:
        source_input = Path("example.txt")
    else:
        source_input = Path("input.txt")    
    
    
    if args.parts.upper() == "AB":
        part_a, part_b = main(source_input, do_a=True, do_b=True)
    elif args.parts.upper() == "A":
        part_a, part_b = main(source_input, do_a=True, do_b=False)
    elif args.parts.upper() == "B":
        part_a, part_b = main(source_input, do_a=False, do_b=True)
    else:
        raise ValueError(f"unknown argument value for 'parts': {args.parts}")
        

