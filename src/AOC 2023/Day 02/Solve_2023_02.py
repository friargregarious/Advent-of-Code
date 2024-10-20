"""
#                              ADVENT OF CODE: 2023
#                                 Cube Conundrum
#                      https://adventofcode.com/2023/day/2
###############################################################################
# SOLVER:   friargregarious (greg.denyes@gmail.com)
# SOLVED:   {#SOLVED}
# HOME:     https://github.com/friargregarious
# SOURCE:   https://github.com/friargregarious/AOC-2023
# WRITTEN AND TESTED IN PYTHON VER 3.11.6
"""

###############################################################################
# IMPORTS AND DECLARATIONS
###############################################################################

import os
from configparser import ConfigParser
import math
from termcolor import colored
import aocd

os.system("cls")

__RUN_ON_EXAMPLE__ = False
YEAR, DAY = 2023, 2
CENTERING = 100
BANNER = "^".center(CENTERING, "-")
LIMITS = {"red": 12, "blue": 14, "green": 13}
ANS_EXAMPLE_A = 8
ANS_EXAMPLE_B = 2286

""" EXAMPLE.TXT
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

###############################################################################
# DATA MANIPULATION
###############################################################################


def parse_data(source):
    # builds data structure for all given inputs
    if source.endswith(".txt"):
        raw = open(source).read().split("\n")
    else:
        raw = source.split("\n")

    results = {}

    print(" Parsing Input Data ".center(CENTERING, "-"))
    for row in raw:
        # if len(raw) > 5:
        game_id, game_data = row.split(": ")
        results[game_id] = {"red": [], "green": [], "blue": []}

        for rounds in game_data.split("; "):
            # print("Round:", rounds)
            for colour in rounds.split(", "):
                qty, clr = colour.split(" ")
                # print("qty:", qty, "colour", clr)
                results[game_id][clr].append(int(qty))

        print(game_id.rjust(10), results[game_id])
    return results


###############################################################################
# SOLVE FOR PART A
###############################################################################


def solve_a(games):
    """determine how many games from the data list would be possible
    based on the limits provided."""
    # games = parse_data(data)
    print(" Solving Part A ".center(CENTERING, "-"))

    running_total = 0
    solution = {}
    for game_id, colours in games.items():
        solution[game_id] = {"red": None, "green": None, "blue": None}
        c_msgs = []
        for this_colour, res in colours.items():
            answer = max(res) < LIMITS[this_colour]
            if not answer:
                selcolr = "red"
            else:
                selcolr = "green"
            p_msg = colored(f"Answer: {answer}".ljust(15), selcolr)
            p_msg += f"Max {this_colour}: {max(res)}".rjust(15)
            p_msg += f" < {LIMITS[this_colour]} Limit.".rjust(15)

            c_msgs.append(p_msg.center(CENTERING))

            solution[game_id][this_colour] = answer

        possible = all(solution[game_id].values())
        if possible:
            selcolr = "green"
            running_total += int(game_id.split(" ")[-1])
        else:
            selcolr = "red"

        g_msg = f"{game_id}: " + colored("Possible", selcolr)
        g_msg += f" Running Total: {running_total}"
        print(g_msg.center(CENTERING))
        print("\n".join(c_msgs))
    print(f"A Final: {running_total}".center(CENTERING))
    return running_total


###############################################################################
# SOLVE FOR PART B
###############################################################################


def solve_b(games):
    """determine the minimum # of cubes necessary to play each game
    multiply those minimums together into one product for each game
    sum all the products
    return the sum
    """
    print(" Solving Part B ".center(CENTERING, "-"))

    biggest, products = {}, {}
    for game_id, colours in games.items():
        biggest[game_id] = []
        for _, res in colours.items():
            biggest[game_id].append(max(res))
        products[game_id] = math.prod(biggest[game_id])

        big_str = [str(y) for y in biggest[game_id]]

        msg = f"{game_id}:".rjust(8)
        msg += f"{products[game_id]} = ".rjust(10)
        msg += " X ".join(big_str).ljust(13)
        print(msg.center(CENTERING))
    sum_of_products = sum(products.values())
    print(f"B Final: {sum_of_products}".center(CENTERING))

    return sum_of_products


###############################################################################
# ENTRY POINT FOR SUBMITTING & BENCHMARKING


def main(source):
    return (solve_a(source), solve_b(source=source))


###############################################################################
# COLLECT RESULTS AND TEST AGAINST PUZZLE OR EXAMPLE

if __name__ == "__main__":
    # __RUN_ON_EXAMPLE__ = True

    if __RUN_ON_EXAMPLE__:
        PARSED = parse_data("example.txt")

        solution_a = solve_a(PARSED)
        solution_b = solve_b(PARSED)

        result_a = solution_a == ANS_EXAMPLE_A
        result_b = solution_b == ANS_EXAMPLE_B

        ############################################################
        # test solution for A

        temp = "My Part A Example Solution:"
        r_msg = [BANNER, temp.center(CENTERING)]

        if result_a:
            temp = f"{solution_a} Matches {ANS_EXAMPLE_A}"
            r_msg.append(colored(temp.center(CENTERING), "green"))
        else:
            temp = f"{solution_a} Does NOT Match {ANS_EXAMPLE_A}"
            r_msg.append(colored(temp.center(CENTERING), "red"))

        r_msg.append(BANNER)
        print("\n".join(r_msg))

        ############################################################
        # test solution for B
        temp = "My Part B Example Solution:"
        r_msg = [BANNER, temp.center(CENTERING)]

        if result_b:
            temp = f"{solution_b} Matches {ANS_EXAMPLE_B}"
            r_msg.append(colored(temp.center(CENTERING), "green"))
        else:
            temp = f"{solution_b} Does NOT Match {ANS_EXAMPLE_B}"
            r_msg.append(colored(temp.center(CENTERING), "red"))

        r_msg.append(BANNER)
        print("\n".join(r_msg))

    else:
        PARSED = parse_data("input.txt")

        solution_a = solve_a(PARSED)
        solution_b = solve_b(PARSED)

        ############################################################
        # submit answers to AOC

        cfg = ConfigParser()
        cfg.read(".env")
        token = cfg.get("user", "token")

        me = aocd.models.User(token)
        puzzle = aocd.models.Puzzle(YEAR, DAY, me)
        # puzzle.answer_a = solution_a
        if puzzle.answered_a:
            puzzle.answer_b = solution_b
        else:
            puzzle.answer_a = solution_a
