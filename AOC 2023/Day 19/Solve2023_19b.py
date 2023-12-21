"""
#                  ADVENT OF CODE | 2023 | APLENTY | PART [B]                 #
#                         adventofcode.com/2023/day/19                        #
# SOLVER: --------------------------------------------------- friargregarious #
# CONTACT: --------------------------------------- friar.gregarious@gmail.com #
# HOME: -------------------------------------------------------------- github #
# SOURCE: ---------------------------------- ~/Advent-of-Code/AOC 2023/Day 19 #
# WRITTEN AND TESTED IN: --------------------------------------------- 3.11.6 #
"""
###############################################################################
# IMPORTS #####################################################################
###############################################################################

import os

from configparser import ConfigParser

# import my_utilities

# import math
from datetime import datetime

from termcolor import colored
import aocd

###############################################################################
# DECLARATIONS ################################################################
###############################################################################

__version__ = "0.0.0"
__example_answer__ = None
__run_on_example__ = False
year, day = 2023, 19
###############################################################################
# GATHER_TOOLS ################################################################
###############################################################################

from Solve2023_19a import MyPart, WorkFlow, parse_input, report_parts, job_is_done


def generate_parts():
    min_rating, max_rating = 1, 4000
    for x in range(min_rating, max_rating + 1):
        for m in range(min_rating, max_rating + 1):
            for a in range(min_rating, max_rating + 1):
                for s in range(min_rating, max_rating + 1):
                    this_part = {"x": x, "m": m, "a": a, "s": s}
                    yield MyPart(this_part)


###############################################################################
# SOLVE PART B ################################################################
###############################################################################


def solve_b(data):
    """For solving PART b of day 19's puzzle."""
    _, work_flows = parse_input(data)
    # report_parts(pile_of_parts)

    # actual_targets = set()
    # worker_addresses = set()
    # max_mins = {}
    # for address, worker in work_flows.items():
    #     worker_addresses.add(address)
    #     actual_targets.add(worker.default)
    #     for rule, target in worker.rules:
    #         actual_targets.add(target)
    #         if target == "R":
    #             if ">" in rule:
    #                 check, val = rule.split(">")
    #                 if f"min_{check}" not in max_mins:
    #                     max_mins[f"min_{check}"] = []
    #                 max_mins[f"min_{check}"].append(val)
    #             if "<" in rule:
    #                 check, val = rule.split("<")
    #                 if f"max_{check}" not in max_mins:
    #                     max_mins[f"max_{check}"] = []
    #                 max_mins[f"max_{check}"].append(val)

    # unused_targets = worker_addresses.difference(actual_targets)
    # print("we aren't using these flows at all:", unused_targets)

    # _ = input()
    # for x in unused_targets:
    #     del work_flows[x]

    total_checked, total_accepted = 0, 0
    total_possibilities = 4_000**4
    # while not job_is_done(pile_of_parts):
    start_stamp = datetime.now()
    for part in generate_parts():
        total_checked += 1
        if total_checked % 50_000 == 0:
            os.system("cls")
            l_col = 16
            r_col = 22
            elapsed = datetime.now() - start_stamp  # .  .strftime(format="%H:%M:%S")

            hours = int(elapsed.total_seconds() / (60*60))
            remaining_seconds = elapsed.total_seconds() - (hours * 60 * 60)
            minutes = int(remaining_seconds / 60)
            remaining_seconds = int(elapsed.total_seconds() - (minutes * 60))

            rep_parts = [
                ("Time Elapsed", f"{hours}:{minutes:02}:{remaining_seconds:02}"),
                ("Total Possible", f"{total_possibilities:,}"),
                ("Total Completed", f"{total_checked:,}"),
                ("Total Accepted", f"{total_accepted:,}"),
                ("Total Rejected", f"{total_checked - total_accepted:,}"),
                ("Total Remaining", f"{total_possibilities-total_checked:,}"),
            ]
            print("".ljust(l_col + r_col + 3, "-"))
            for rmsg, lmsg in rep_parts:
                print(lmsg.rjust(r_col) + " : " + rmsg.ljust(l_col))
            print("".ljust(l_col + r_col + 3, "-"))

        while True:  # part.path[-1] not in ["A", "R"]:
            worker = part.path[-1]
            part.path.append(work_flows[worker].test(part))

            if part.path[-1] == "A":
                total_accepted += 1
                break
            if part.path[-1] == "R":
                break

    # solution = data

    return total_accepted


###############################################################################
# MAIN ENTRY POINT FOR SUBMITTING AND BENCHMARKING ############################
###############################################################################


def main(source):
    """Main entry point"""
    if __run_on_example__:
        return solve_b("example.txt")
    return solve_b(source)


###############################################################################
# RUNNING_FROM_HOME ###########################################################
###############################################################################

if __name__ == "__main__":
    os.system("cls")

    __run_on_example__ = True

    # data = open("example.txt", encoding="utf-8").read()
    data = open("input.txt", encoding="utf-8").read()
    final_answer_b = main(data)
    # final_answer_a, final_answer_b = main(data)

    if __run_on_example__:
        print(
            f"My answer [{final_answer_b}] is correct:",
            final_answer_b == __example_answer__,
        )

    else:
        cfg = ConfigParser()
        cfg.read(".env")
        token = cfg.get(section="user", option="token")
        me = aocd.models.User(token)
        this_puzzle = aocd.models.Puzzle(year, day, user=me)

        this_puzzle.answer_b = final_answer_b
