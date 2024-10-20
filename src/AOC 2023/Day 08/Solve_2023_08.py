###############################################################################
#
#                              ADVENT OF CODE: 2023
#                               Haunted Wasteland
#                      https://adventofcode.com/2023/day/8
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
from datetime import datetime
from termcolor import colored
import aocd


###############################################################################
# GATHER TOOLS ################################################################
###############################################################################


# Starting with `AAA`, you need to *look up the next element* based on the next
# left/right instruction in your input. In this example, start with `AAA` and
# go *right* (`R`) by choosing the right element of `AAA`, `CCC`. Then, `L`
# means to choose the *left* element of `CCC`, `ZZZ`. By following the
# left/right instructions, you reach `ZZZ` in `2` steps.


###############################################################################
# PART A ######################################################################
###############################################################################
def next_step(map_key):
    """return the index of the location we'd like to go to next"""
    i = 0  # Start from the beginning of the string
    while True:
        yield 1 if map_key[i] == "R" else 0
        i = (i + 1) % len(
            map_key
        )  # Move to the next character, and wrap around if the end is reached


report = []


def solve_a(source):
    """Solving for part A"""
    report.append("Solving for part A")

    end_point = "ZZZ"
    map_key = next_step(source["map_key"])
    travel_log = ["AAA"]
    current_position = travel_log[-1]

    while not (current_position == end_point):
        direction = next(map_key)
        next_location = source[current_position][direction]
        travel_log.append(next_location)
        current_position = travel_log[-1]

    solution = len(travel_log) - 1

    # report.append(" --> ".join(travel_log))
    report.append(f"Part A Solution: {solution}")
    for row in report:
        print(row)

    return solution


###############################################################################
# PART B ######################################################################
###############################################################################


def all_done(t_log: list):
    """if this is a container of paths,
    then return the completed state for all paths
    within the contain.
    """
    return all([x.endswith("Z") for x in t_log])


def solve_b(source):
    """Ghost Travel?"""
    start_b = datetime.now()

    report.append("Solution B: Ghost Travel?")
    # source = parse(open("exampleB.txt").read())

    # starting point(s) are source.keys() that end in A
    travel_log = []
    map_key = next_step(source["map_key"])

    # we will start by pulling out all the starting points and putting them
    # into seperate lists within travel_log.

    for key in source.keys():
        if key.endswith("A"):
            travel_log.append(key)

    report.append(f"Travel Log B contains {len(travel_log)} paths.")

    #  then every iteration of the main
    # loop will append the next step to that path.
    steps_taken = 0

    prev_direction = source["map_key"][0]

    report_msg = "\n".join(report)
    ll_instances = {}

    def min_sec(seconds: float):
        """for time stamps"""
        return int(seconds) // 60, int(seconds) % 60

    while not all_done(travel_log):
        direction = next(map_key)

        last_letters = [x[-1] for x in travel_log]
        ll_cnt = last_letters.count("Z")
        # if ll_cnt in [3, 4, 5, 6]:
        if ll_cnt not in ll_instances:
            ll_instances[ll_cnt] = 0
        ll_instances[ll_cnt] += 1

        # report.append(f"  @ --> {steps_taken} there were {x} finishers")

        # if last_letters.count("Z") >= len(last_letters) // 3:
        if steps_taken % 2_000_000 == 0:
            statusmsg = "-" * 40
            # statusmsg += f"\ncurrent direction: {direction} with {dir_changes} direction changes"
            # statusmsg += (
            #     f"\nCurrent Positions: {', '.join([str(x) for x in travel_log])}"
            # )
            # statusmsg += f"\n Current Last letters:  { ', '.join([x[-1] for x in travel_log])}"
            mins, secs = min_sec((datetime.now() - start_b).total_seconds())
            statusmsg += (
                f"\nProcess B has taken {steps_taken:,} steps in {mins:,} m & {secs} s."
            )
            for k, v in ll_instances.items():
                if k > 0:
                    statusmsg += f"\n-->  {v:,} instances of {k} finishers"
            # _ = input()
            os.system("cls")
            print(report_msg)
            print(statusmsg)

        for current_path in travel_log.copy():
            # current_position = current_path[-1]
            travel_log.append(source[travel_log.pop(0)][direction])

        steps_taken += 1

    return steps_taken


###############################################################################
# MAIN ENTRY POINT FOR SUBMITTING & BENCHMARKING ##############################
###############################################################################
def parse(raw_data):
    """I'm going to start doing all the parsing here from now on."""
    map_instructions = {"starting_points": 0, "ending_points": 0}

    for index, row in enumerate(raw_data.split("\n")):
        if index == 0:
            map_instructions["map_key"] = row.strip()
        if index > 1 and len(row) > 1:
            inst_key, dirtemp = row.split(" = ")
            if inst_key.endswith("A"):
                map_instructions["starting_points"] += 1
            if inst_key.endswith("Z"):
                map_instructions["ending_points"] += 1

            directions = dirtemp.strip("()").split(", ")
            map_instructions[inst_key] = tuple(directions)

    return map_instructions


def main(source):
    ready_data = parse(source)
    report.append(
        f"Parsed data has: {ready_data['starting_points']} start points"
        + f" and {ready_data['ending_points']} end points."
    )

    # return (solve_a(source=ready_data), solve_b(source=ready_data))
    return (solve_a(source=ready_data), 0)
    # return (0, 0)


###############################################################################
# RUNNING FROM HOME ###########################################################
###############################################################################
if __name__ == "__main__":
    THISYEAR, THISDAY = 2023, 8
    # set the example flag here
    EXAMPLE = False
    # EXAMPLE = True
    C_ANS_A = 6
    C_ANS_B = 6

    # os.system("cls")
    # root = os.getcwd().replace("\\", "/")
    # exe_msg = f"{root}/my_utilities/reporting.py -y {THISYEAR} -d {THISDAY}"

    # if EXAMPLE:
    #     exe_msg += f" -e '{C_ANS_A},{C_ANS_B}'"

    # os.system(exe_msg)

    if EXAMPLE:
        data = open("example2.txt", encoding="utf-8").read()
    else:
        data = open("input.txt", encoding="utf-8").read()

    final_answer_a, final_answer_b = main(data)

    if EXAMPLE:
        for row in [("A", 6, final_answer_a), ("B", 6, final_answer_b)]:
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
        cfg.read("C:/Advent of Code/.env")
        token = cfg.get(section="friargregarious", option="token")
        me = aocd.models.User(token=token)
        this_puzzle = aocd.models.Puzzle(THISYEAR, THISDAY, user=me)

        if this_puzzle.answered_a:
            this_puzzle.answer_a = final_answer_a

        if not this_puzzle.answered_b:
            this_puzzle.answer_b = final_answer_b
