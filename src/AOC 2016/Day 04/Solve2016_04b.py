"""
#        ADVENT OF CODE | 2016 | SECURITY THROUGH OBSCURITY | PART [B]        #
#                         adventofcode.com/2016/day/4                         #
# SOLVER: --------------------------------------------------- friargregarious #
# CONTACT: --------------------------------------- friar.gregarious@gmail.com #
# HOME: -------------------------------------------------------------- github #
# SOURCE: ----------------------------------- ~/Advent-of-Code/AOC 2016/Day 4 #
# WRITTEN AND TESTED IN: --------------------------------------------- 3.13.0 #
"""
###############################################################################
# IMPORTS #####################################################################
###############################################################################

import os
import argparse
import my_utilities
import re
from pathlib import Path
from string import ascii_letters, ascii_lowercase

# import math
# from datetime import datetime
# from termcolor import colored
# import aocd

###############################################################################
# DECLARATIONS ################################################################
###############################################################################
__year__ = 2016
__day__ = 4
__build__ = 37
__version__ = "0.0.37" 
__example_answer__ = 1514
__run_on_example__ = False

###############################################################################
# GATHER_TOOLS ################################################################
###############################################################################


def parse_input(source: str):
    """For parsing source string into usable content"""
    return list(Path(source).read_text(encoding="utf-8").split("\n"))


###############################################################################
# SOLVE PART A ################################################################
###############################################################################


def is_a_room(left, right):
    counts = {}
    new_counts = {}

    for c in left:
        if c in ascii_letters:
            if c in counts:
                counts[c] += 1
            else:
                counts[c] = 1
    
    for k, v in counts.items():
        if v in new_counts:
            new_counts[v] += k
        else:
            new_counts[v] = k
            
    new_counts = {k : "".join(sorted(v)) for k, v in new_counts.items()}
    key = sorted(set(counts.values()), reverse=True)
    
    new_counts = {k: new_counts[k] for k in key}    
    
    new_order = ""
    for k, v in new_counts.items():
        new_order += v

    new_order = new_order[:5]

    return new_order==right
    

def solve_a(data):
    """For solving PART a of day 4's puzzle."""
    print(print_version())
    solution = 0
    
    # aaaaa-bbb-z-y-x-123[abxyz]
    # a-b-c-d-e-f-g-h-987[abcde]
    # not-a-real-room-404[oarel]
    # totally-real-room-200[decoy]

    good_rooms = []
    for row in data:
        words = row.split("-")

        num, right = words[-1].split("[")
        order = right.strip("]")
        num = int(num)

        words = "-".join(words[:-1])

        order = row[ row.find("[")+1 : row.find("]") ]
        

        if is_a_room(words, order):
            good_rooms.append((words, num, order))
    
        
    # return solution
    return good_rooms


def solve_b(data):
    goodrooms = solve_a(data)
    
    for room, key, order in goodrooms:
        room_name = ""
        for c in room:  # character in room name
            if c == "-":
                room_name += " "
            elif c in ascii_lowercase:
                
                shift = ascii_lowercase.index(c) + (key % len(ascii_lowercase))
                if shift >= len(ascii_lowercase):
                    shift -= len(ascii_lowercase)
                
                room_name += ascii_lowercase[shift]
        print(key, room_name) if "northpole object storage" == room_name else None

###############################################################################
# MAIN ENTRY POINT FOR SUBMITTING AND BENCHMARKING ############################
###############################################################################
def main(source):
    """Main entry point"""
    return solve_b(source)


###############################################################################
# RUNNING_FROM_HOME ###########################################################
###############################################################################

def print_version():
    fname = f"AOC {__year__} Day {__day__}"
    return f"Program: ({fname}) Version: {__version__} Build: {__build__:04}"
    
    
    
if __name__ == "__main__":
    os.system("cls")
    # parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(
                        prog=f'{__file__}',
                        description=f'Solves puzzle for inputs provided on AOC {__year__} Day {__day__}.',
                        epilog='Only used within the AOC Enviroment.')

    # parser.add_argument(
    #     "solve", 
    #     help="A or B, Default Runs on A.", 
    #     default="A", 
    #     action=main())
    
    parser.add_argument(
        "-e", 
        "--example", 
        help="Run This Solve on example input. Default is regular input.", 
        action='store_true', 
        default=False)

    parser.add_argument(
        "-v", 
        "--version", 
        help="Returns the current version of this file.", 
        action='version', 
        version=print_version())
    
    args = parser.parse_args()

    __run_on_example__ = args.example
    print(f"Run on example: {__run_on_example__}")
    my_utilities.version_increment(__file__, sml=1)

    if __run_on_example__:
        example_path = str(Path(__file__).parent / "example.txt")
        src = parse_input(example_path)
    else:
        input_path = str(Path(__file__).parent / "input.txt")
        src = parse_input(input_path)

    # print(f"Solving: {args.solve}")
    answer = main(source=src)    
    print(answer)
    # my_utilities.solve_a()