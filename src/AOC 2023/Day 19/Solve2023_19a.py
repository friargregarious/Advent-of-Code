"""
#                  ADVENT OF CODE | 2023 | APLENTY | PART [A]                 #
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
import aocd

# import my_utilities

# import math
# from datetime import datetime
# from termcolor import colored

###############################################################################
# DECLARATIONS ################################################################
###############################################################################

__version__ = "0.0.2"
__example_answer__ = 19114
__run_on_example__ = False
year, day = 2023, 19


###############################################################################
# GATHER_TOOLS ################################################################
###############################################################################
class MyPart:
    """simple object to represent a gear and it's XMAS rating"""

    def __init__(self, inputs: dict) -> None:
        # these are likely unnessessary
        self.x = inputs["x"]
        self.m = inputs["m"]
        self.a = inputs["a"]
        self.s = inputs["s"]
        self.path = ["in"]
        self.value = sum(inputs.values())

    def __str__(self) -> str:
        # for_printing = [x.rjust(3) for x in self.path]
        return f"Gear [{self.value}]: " + "{" + ", ".join(self.path) + "}"
        # # assigns values to properties
        # self.__dict__.update(inputs)


class WorkFlow:
    def __init__(self, parts: list) -> None:
        self.rules = []  # key is rule to eval, val is target to send to
        # list of MyPart(gear)'s to work on, pop(0) to keep them in order
        self.queue = []
        self.default = ""  # default target if no other rules apply

        self.default = parts[-1]
        for rules in parts[:-1]:
            evaluator, target = rules.split(":")
            self.rules.append((evaluator, target))

    def test(self, gear) -> str:
        # this_gear = MyPart(gear)
        for rule_evaluation, target in self.rules:
            # print(rule_evaluation, target)
            eval_this_line = f"gear.{rule_evaluation}"
            resolution = eval(eval_this_line)
            # print(current rule: {rule_evaluation})
            # print(f"Evaluating {gear} for: {eval_this_line} [{resolution}]")

            if resolution:
                # print("sending to:", target)
                return target

        # print("sending to:", target)
        return self.default


def report_parts(part_list):
    print("".center(60, "-"))
    for part in part_list:
        print(part)


def job_is_done(part_list):
    return all([part.path[-1] in ["A", "R"] for part in part_list])


def parse_input(source: str = "input.txt"):
    """For parsing source string into usable content"""
    if source.endswith(".txt"):
        raw = open(source).read().split("\n")
    else:
        raw = source.split("\n")

    p_list, wf_dict = [], {}

    for row in raw:
        if len(row) > 0:
            if row[0].isalpha():  # this is a workflow
                key, parts = row.split("{")
                parts = parts.strip("}").split(",")

                wf_dict[key] = WorkFlow(parts)

                # work_flows[key].append(new_flow)
                # print(work_flows[key])

            elif row.startswith("{"):  # these are parts
                new_part = {}
                this_line = row.replace("}", "").replace("{", "")
                for pair in this_line.split(","):
                    key, val = pair.split("=")
                    new_part[key] = int(val)

                p_list.append(MyPart(new_part))

            else:
                print(f"Didn't find case for [{row}]")
    return p_list, wf_dict


###############################################################################
# SOLVE PART A ################################################################
###############################################################################


def solve_a(data):
    """For solving PART a of day 19's puzzle."""
    pile_of_parts, work_flows = parse_input(data)

    report_parts(pile_of_parts)

    while not job_is_done(pile_of_parts):
        for part in pile_of_parts:
            if part.path[-1] not in ["A", "R"]:
                worker = part.path[-1]
                part.path.append(work_flows[worker].test(part))
        report_parts(pile_of_parts)

    solution = sum([part.value for part in pile_of_parts if part.path[-1] == "A"])
    print(f"Final answer for a is: {solution}")

    return solution


###############################################################################
# MAIN ENTRY POINT FOR SUBMITTING AND BENCHMARKING ############################
###############################################################################


def main(source):
    """Main entry point"""
    if __run_on_example__:
        return solve_a("example.txt")
    return solve_a(source)


###############################################################################
# RUNNING_FROM_HOME ###########################################################
###############################################################################

if __name__ == "__main__":
    os.system("cls")

    # __run_on_example__ = True

    # data = open("example.txt", encoding="utf-8").read()
    data = open("input.txt", encoding="utf-8").read()
    final_answer_a = main(data)
    # final_answer_a, final_answer_b = main(data)

    if __run_on_example__:
        print(
            f"My answer [{final_answer_a}] is correct:",
            final_answer_a == __example_answer__,
        )

    else:
        cfg = ConfigParser()
        cfg.read(".env")
        token = cfg.get(section="user", option="token")
        me = aocd.models.User(token)
        this_puzzle = aocd.models.Puzzle(year, day, user=me)

        this_puzzle.answer_a = final_answer_a
