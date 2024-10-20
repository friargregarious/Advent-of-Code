###############################################################################
#
#                              ADVENT OF CODE: 2023
#                                  Wait For It
#                      https://adventofcode.com/2023/day/6
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
import math
from configparser import ConfigParser
import aocd


###############################################################################
# SETUP THE TOOLS


def a_parse_input(source_data=None, example=False):
    """
    This document describes three races:
        The first race lasts 7 milliseconds.
        The record distance in this race is 9 millimeters.

        The second race lasts 15 milliseconds.
        The record distance in this race is 40 millimeters.

        The third race lasts 30 milliseconds.
        The record distance in this race is 200 millimeters.
    """
    raw = source_data.strip("\n").split("\n")

    body = {}
    for line in raw:
        key, num_string = line.split(":")
        # body[key]=num_string
        splitline = num_string.split(" ")
        body[key] = [int(x) for x in splitline if x.isdigit()]

    result = {}
    for x, tup in enumerate(zip(body["Time"], body["Distance"])):
        result[x + 1] = tup

    return result


def b_parse_input(source_data):
    """
    As the race is about to start, you realize the piece of paper with race
    times and record distances you got earlier actually just has very bad
    kerning. There's really only one race
    - ignore the spaces between the numbers on each line.
    """
    raw = source_data.strip("\n").split("\n")

    a_time = 0
    r_dist = 0
    for line in raw:
        key, num_string = line.split(":")
        if key == "Time":
            a_time = int(num_string.replace(" ", ""))
        else:
            r_dist = int(num_string.replace(" ", ""))

    return (a_time, r_dist)


def calc_charge_vs_distance(alloted_time):
    """
    Your toy boat has a starting speed of zero mm/ms.
    For each whole ms you spend at the beginning of the race holding
    down the button, the boat's speed increases by one mm/ms.

    So, because the first race lasts 7 ms, you only have a few options:

        * Don't hold the button at all. The boat won't move;
        hold it for 0 ms =                    by the end of the race  0 mm
        Hold for    1 ms = 1 mm/ms for 6 remaining ms total distance  6 mm
        Hold for    2 ms = 2 mm/ms for 5 remaining ms total distance 10 mm
        Hold for    3 ms = 3 mm/ms for 4 remaining ms total distance 12 mm
        Hold for    4 ms               3 ms                          12 mm
        Hold for    5 ms                                             10 mm
        Hold for    6 ms                                              6 mm
        Hold for    7 ms    That's the entire duration of the race    0 mm
    """
    possible_outcomes = {}
    for x in range(alloted_time):
        # alloted_time is alloted time for race
        c_time = x  # time spent charging
        m_time = alloted_time - c_time  # time remaining to move
        t_dist = m_time * c_time  # total distance traveled
        possible_outcomes[x] = (t_dist, m_time, c_time)
    return possible_outcomes


def ways_to_win(outcomes, race_record):
    """
    Since the current record for this race is 9 millimeters,
    there are actually 4 different ways you could win:
        hold for 2, 3, 4, or 5 ms

    In the second race,
        hold for at least 4 ms and
                 at most 11 ms and
        beat the record, a total of 8 different ways to win.

    In the third race,
        hold for at least 11 ms and
                 at most  19 ms and
        still beat the record, a total of 9 ways you could win.
    """

    # possible_outcomes[x] = (t_dist, m_time, c_time)
    successes = {}
    for k, v in outcomes.items():
        t, m, c = v
        if t > race_record:
            successes[k] = (t, m, c)

    return successes


###############################################################################
# To see how much margin of error you have, determine the number of ways you
# can beat the record in each race; in this example, if you multiply these
# values together, you get 288 (4 * 8 * 9).
# Determine the number of ways you could beat the record in each race. What
# do you get if you multiply these numbers together?


def solve_a(source):
    """placeholder"""

    total_successes = []
    for k, v in source.items():
        time, dist = v

        possibe_outcomes = calc_charge_vs_distance(time)
        winning_outcomes = ways_to_win(possibe_outcomes, dist)
        total_successes.append(len(winning_outcomes))

        msg = f"Race #{k} Time Allowed: {time} Record Distance: {dist}\n"
        msg += f"Successes {len(winning_outcomes)} "
        msg += f"/ Total Possibilities: {len(possibe_outcomes)}."
        # msg += f"Possible Outcomes: {possibe_outcomes}\n"
        # msg += f"Winning Outcomes: {winning_outcomes}\n"

        print(msg)

    solution = math.prod(total_successes)
    print("Solution A:", solution)

    # outcomes = [calc_charge_vs_distance(t) for t[0] in races]
    # print(races, "\n", outcomes)

    return solution


###############################################################################
# {example 2}


def solve_b(source):
    """placeholder"""
    alloted_time, record_distance = source
    total_successes: int = 0
    print("B Data:", source)
    for x in range(alloted_time):
        # alloted_time is alloted time for race
        c_time = x  # time spent charging
        m_time = alloted_time - c_time  # time remaining to move
        t_dist = m_time * c_time  # total distance traveled

        if t_dist > record_distance:
            total_successes += 1

    print("Solution B:", total_successes)

    return total_successes


###############################################################################
# ENTRY POINT FOR SUBMITTING & BENCHMARKING


def main(source=None):
    """entry point for aocd benchmarking,
    also: if running __main__ then we can
    force the data set here.
    """

    if source is None:
        file = open("input.txt", encoding="utf_8").read()
        parsed_a = a_parse_input(file)
        parsed_b = b_parse_input(file)
    else:
        parsed_a = a_parse_input(source)
        parsed_b = b_parse_input(source)

    a_answer = solve_a(parsed_a)
    b_answer = solve_b(parsed_b)

    return (a_answer, b_answer)


if __name__ == "__main__":
    os.system("cls")
    # data = open("example.txt", encoding="utf-8").read()
    data = open("input.txt", encoding="utf-8").read()
    final_answer_a, final_answer_b = main(data)
    # main()

    cfg = ConfigParser()
    cfg.read("C:/Advent of Code/.env")
    token = cfg.get(section="friargregarious", option="token")
    me = aocd.models.User(token=token)
    this_puzzle = aocd.models.Puzzle(year=2023, day=6, user=me)

    if not this_puzzle.answered_a:
        this_puzzle.answer_a = final_answer_a
    if not this_puzzle.answered_b:
        this_puzzle.answer_b = final_answer_b
