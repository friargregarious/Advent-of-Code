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
from pathlib import Path

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


def solve_a(source):
    """Oasis And Sand Instability Sensor"""
    prediction_sum = 0
    for sequence in source:

        while True:
            # Calculate the differences between consecutive numbers in the sequence
            differences = [
                sequence[i] - sequence[i - 1] for i in range(1, len(sequence))
            ]

            # If the differences are all zeroes, we can predict the next value
            if all(d == 0 for d in differences):

                # The next value is the last value in the sequence plus the last difference
                next_value = sequence[-1] + differences[-1]
                prediction_sum += next_value

            # Otherwise, repeat the process with the differences as the new sequence
            sequence = differences

    return prediction_sum


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
        # print(reading)
        # if len(reading) > 1:
        converted = list(map(int, reading.split(" ")))
        # print(converted)
        sensor_history.append(converted)
    return sensor_history


def main(raw):
    """main entry point"""
    processed = parse(raw.split("\n"))

    return (solve_a(source=processed), solve_b(source=processed))


if __name__ == "__main__":
    source = Path("input.txt").read_text().split("\n")
    print(solve_a(parse(source)))
