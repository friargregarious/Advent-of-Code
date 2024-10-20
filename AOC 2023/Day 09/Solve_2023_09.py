###############################################################################
#
#                              ADVENT OF CODE: 2023
#                               Mirage Maintenance
#                      https://adventofcode.com/2023/day/9
#
###############################################################################
#
# SOLVER:   friargregarious (greg.denyes@gmail.com)
# SOLVED:   {#SOLVED}
# HOME:     https://github.com/friargregarious
# SOURCE:   https://github.com/friargregarious/AOC-2023
#
# WRITTEN AND TESTED IN PYTHON VER 3.11.6
#

###############################################################################
# IMPORTS #####################################################################
###############################################################################

import os
from configparser import ConfigParser

# import math
# from datetime import datetime
from termcolor import colored
import aocd

###############################################################################
# GATHER TOOLS ################################################################
###############################################################################


from tools import Prediction, line_results


###############################################################################
# PART A ######################################################################
###############################################################################
class my_runner:
    total = 0

def solve_a(source):
    """Oasis And Sand Instability Sensor"""
    # first we extrapolate till zeros
    running_total = my_runner()
    answers = [Prediction(page, running_total).answer for page in source]
    print("# of predictions:", len(answers))
    open("lineresults.txt", "w").write("\n".join(line_results))
    solution = sum(answers)

    return solution


###############################################################################
# PART B ######################################################################
###############################################################################


def solve_b(source):
    return 0


###############################################################################
# MAIN ENTRY POINT FOR SUBMITTING & BENCHMARKING ##############################
###############################################################################
def parse(source):
    """parses the list of strings into integers"""
    sensor_history = []
    for reading in source:
        if len(reading) > 1:
            sensor_history.append([int(x) for x in reading.split(" ")])
    return sensor_history


def main(raw):
    """main entry point"""
    processed = parse(raw.split("\n"))

    return (solve_a(source=processed), solve_b(source=processed))


###############################################################################
# RUNNING FROM HOME ###########################################################
###############################################################################
if __name__ == "__main__":
    THISYEAR, THISDAY = 2023, 9
    # set the example flag here
    EXAMPLE = False
    # EXAMPLE = True
    C_ANS_A = 114
    C_ANS_B = 6

    os.system("cls")
    # root = os.getcwd().replace("\\", "/")
    # exe_msg = f"{root}/my_utilities/reporting.py -y {THISYEAR} -d {THISDAY}"

    # if EXAMPLE:
    #     exe_msg += f" -e '{C_ANS_A},{C_ANS_B}'"

    # os.system(exe_msg)

    if EXAMPLE:
        data = open("example.txt", encoding="utf-8").read()
    else:
        data = open("input.txt", encoding="utf-8").read()

    final_answer_a, final_answer_b = main(data)

    if EXAMPLE:
        for row in [("A", C_ANS_A, final_answer_a), ("B", C_ANS_B, final_answer_b)]:
            part, c_answer, my_answer = row
            is_good = my_answer == c_answer

            if is_good:
                msg = f"Your answer for {part}: {my_answer} is CORRECT!!"
                CLR = "green"

            if not is_good:
                msg = f"Your answer for {part}: {my_answer} is NOT CORRECT!!\n"
                msg += f"The correct answer is {c_answer}"
                CLR = "red"

            print(colored(msg, color=CLR))

    else:
        cfg = ConfigParser()
        cfg.read("C:/Advent of Code/.unused/.env")
        token = cfg.get(section="friargregarious", option="token")
        me = aocd.models.User(token=token)
        this_puzzle = aocd.models.Puzzle(THISYEAR, THISDAY, user=me)

        if not this_puzzle.answered_a:
            this_puzzle.answer_a = final_answer_a

        elif this_puzzle.answered_a and not this_puzzle.answered_b:
            this_puzzle.answer_b = final_answer_b
        else:
            print("You've answered these puzzles already!")
