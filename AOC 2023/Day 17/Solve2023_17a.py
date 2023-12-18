"""
#              ADVENT OF CODE | 2023 | CLUMSY CRUCIBLE | PART [A]             #
#                         adventofcode.com/2023/day/17                        #
# SOLVER: --------------------------------------------------- friargregarious #
# CONTACT: --------------------------------------- friar.gregarious@gmail.com #
# HOME: -------------------------------------------------------------- github #
# SOURCE: ---------------------------------- ~/Advent-of-Code/AOC 2023/Day 17 #
# WRITTEN AND TESTED IN: --------------------------------------------- 3.11.6 #
"""
###############################################################################
# IMPORTS #####################################################################
###############################################################################


import os
from random import choice
from termcolor import colored
#  from my_utilities import MyConfigParser as MyCfg
import my_utilities

# import math
# from datetime import datetime
# import aocd

###############################################################################
# DECLARATIONS ################################################################
###############################################################################

__version__ = "0.0.0"
__example_answer__ = 102
__run_on_example__ = False

###############################################################################
# GATHER_TOOLS ################################################################
###############################################################################

def cls():
    os.system('cls')

def parsed(i:str) -> list:
    raw = i.split("\n")
    return raw

def show_map(heat_map, path_taken):
    for y, row in enumerate(heat_map):
        for x, heat in enumerate(row):
            if (y,x) in path_taken:
                print(colored(head, "white", "on_light_red"))
            else:
                print(heat)

def compass(req):
    rose = {
        "NORTH": (-1,0),
        "SOUTH": (+1,0),
        "EAST": (0,+1),
        "WEST": (0,-1),
        (-1,0):"NORTH" ,
        (+1,0):"SOUTH" ,
        (0,+1):"EAST" ,
        (0,-1):"WEST",
        }
    return rose[req]

def is_bearing(mvr):
    return compass(mvr["bearing"])

def change_bearing(mvr, turn):
    match mvr["bearing"]:
        case "NORTH":
            if turn == "LEFT":
                mvr["bearing"] = "WEST"
            elif turn == "RIGHT":
                mvr["bearing"] = "EAST"

        case "SOUTH":
            if turn == "LEFT":
                mvr["bearing"] = "WEST"
            elif turn == "RIGHT":
                mvr["bearing"] = "EAST"

        case "EAST":
            if turn == "LEFT":
                mvr["bearing"] = "NORTH"
            elif turn == "RIGHT":
                mvr["bearing"] = "SOUTH"

        case "WEST":
            if turn == "LEFT":
                mvr["bearing"] = "SOUTH"
            elif turn == "RIGHT":
                mvr["bearing"] = "NORTH"

    return mvr

def step(mvr):
    m_row, m_col = mvr["loc"]
    b_row, b_col = compass(mvr["bearing"])
    return {"loc":(m_row+b_row, m_col+b_col), "bearing":mvr["bearing"]}
    
def is_legal(m_map, mvr):
    wide = len(m_map[0])-1
    tall = len(m_map)
    r,c = mvr["loc"]
    return 0 <= r <= tall and 0 <= c <= wide 

def look(my_map, coord):
    row = my_map[y]
    return int(row[x])

def best_direction(the_map, the_mover):
    available_heats = [look(the_map, the_mover["loc"]) for _]

###############################################################################
# SOLVE PART A ################################################################
###############################################################################


def solve_a(data):
    """For solving PART a of day 18's puzzle."""

    my_map = parsed(data)
    my_mover = {"loc":(0,0),"bearing":"EAST"}
    starting_point=(0,0)
    path_taken = [starting_point]
    end_point = (len(my_map), len(my_map[0]))
    
    paths_taken = set()
    heat_score = 0
    while path_taken[-1] != end_point:
        available = ["LEFT", "RIGHT", "STRAIGHT"]
        valid_choices = []
        for d in available:
            if is_legal(step(change_bearing(my_mover.copy(), d))):
                valid_choices.append(d)
        my_mover = change_bearing(my_mover, choice(choices))
        my_mover.step()
        path_taken.append(my_mover["loc"])
        heat_score += look(my_map, my_mover["loc"])
        show_map(my_map, my_mover)
    
    my_path_value =             
        
        
        
        
    show_map(my_map, path_taken)
    
    
    solution = data

    return solution


###############################################################################
# MAIN ENTRY POINT FOR SUBMITTING AND BENCHMARKING ############################
###############################################################################


def main(source):
    """Main entry point"""
    if __run_on_example__:
        return solve_a("example.txt", __example_answer__)
    return solve_a(source)


###############################################################################
# RUNNING_FROM_HOME ###########################################################
###############################################################################

if __name__ == "__main__":
    os.system("cls")
    my_utilities.version_increment(__file__, sml=1)
    __run_on_example__ = True
    
    answer = main("input.txt")
    my_utilities.version_increment(__file__, sml=1)
    my_utilities.solve_a(answer)
