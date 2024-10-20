###############################################################################
#
#                              ADVENT OF CODE: 2023
#                        If You Give A Seed A Fertilizer
#                      https://adventofcode.com/2023/day/5
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
import aocd
# import math


###############################################################################
# SETUP THE TOOLS

GROUPS = [
    "seed_to_soil",
    "soil_to_fertilizer",
    "fertilizer_to_water",
    "water_to_light",
    "light_to_temperature",
    "temperature_to_humidity",
    "humidity_to_location",
]


class Grouping:
    """place holder"""

    def __init__(self):
        """place holder"""
        self._options = []

    def add_option(self, data_line):
        """stores tuple of digits to options"""
        destination, source, rng = data_line
        # three numbers:
        # the destination range start,
        #       the source range start,
        #               and the range length.
        # DES, SOURCE, RANGE
        # SOIL, SEED, RANGE
        new_option = (source, source + rng, destination)

        self._options.append(new_option)

    def get_target(self, looking_for):
        """place holder"""
        for src_start, src_end, des in self._options:
            if src_start <= looking_for <= src_end:
                target_num = des + (looking_for - src_start)
                return target_num
        return looking_for


def seed_bag_a(seed_list):
    """placeholder"""
    for x in seed_list:
        yield x


def seed_bag_b(seed_list):
    """placeholder"""
    # pairs = seed_list  # [(type,rng), (type,rng),]
    for seed_type, seed_range in seed_list:
        for ctr in range(seed_range):
            yield seed_type + ctr
            # for seed in [seed_type + n for n in range(seed_range)]:
            # yield seed


class Almanac(dict):
    """placeholder"""

    def __init__(self):
        """placeholder"""
        super().__init__()
        self._seed_bag: list = []

    @property
    def seed_bag(self):
        """placeholder"""
        return self._seed_bag

    @seed_bag.setter
    def seed_bag(self, value: list):
        """placeholder"""
        self._seed_bag = value

    def location_from_seed(self, seed):
        """placeholder"""
        work_number = seed
        for item in GROUPS:
            work_number = self[item].get_target(work_number)
        return work_number


def build_almanac(data_source):
    """placeholder"""

    this_almanac = Almanac()
    header_key = ""
    for line in data_source.split("\n"):
        if len(line) >= 1:
            header_line = line[0].isalpha()
            number_line = line[0].isdigit()

            if header_line:
                if line.startswith("seeds: "):
                    seed_list: list = []
                    for x in line.split(": ")[1].split():
                        seed_list.append(int(x))
                    this_almanac.seed_bag = seed_list

                else:
                    header = line.strip(" map:\n").replace("-", "_")
                    this_almanac[header] = Grouping()
                    header_key = header

                    # there's an issue with using out of scope variables
                    # this line does nothing but avoid the red flags
                    if header_key:
                        pass

            if number_line:
                nums = [int(x) for x in line.split()]
                this_almanac[header].add_option(nums)

    return this_almanac


report = {"PART A": [], "PART B": []}
###############################################################################
# {example 1}


def solve_a(source_almanac: Almanac):
    """use the seedbag list straight up"""
    # os.system("cls")
    nearest_loc = 99999999999999999
    seed_count = 0
    for seed in source_almanac.seed_bag:
        seed_count += 1

        my_num = seed
        for layer in source_almanac.values():
            my_num = layer.get_target(my_num)

            if my_num < nearest_loc:
                nearest_loc = my_num

        msg = f"Seed #{seed_count}".ljust(15)
        msg += f"[{seed}]".ljust(15) + " = "
        msg += f"[{my_num}]".ljust(15)
        msg += f"Nearest Location: {nearest_loc}".rjust(35)

        report["PART A"].append(msg)
        if len(report["PART A"]) > 30:
            report["PART A"].pop(0)

        os.system("cls")
        print("PART A TESTS")
        for row in report["PART A"]:
            print("\t", row)

    return nearest_loc


###############################################################################
# {example 2}


def solve_b(source_almanac):
    """
    seeds: 79 14 55 13
    This line describes two ranges of seed numbers to be planted in the
    garden. The first range
    starts with seed number 79 and contains 14
              values: 79, 80, ..., 91, 92.
    The second starts with seed number 55 and contains 13
              values: 55, 56, ..., 66, 67.
    """

    from_seeds = source_almanac.seed_bag
    my_seed_bag = []
    for x, y in zip(from_seeds[::2], from_seeds[1::2]):
        my_seed_bag.append((x, y))

    seed_count = 0
    nearest_loc = 99999999999999999
    for seed, ctr in my_seed_bag:
        for x in range(ctr):
            my_num = seed + x
            seed_count += 1

            for layer in source_almanac.values():
                my_num = layer.get_target(my_num)

            old_nearest = nearest_loc
            if my_num < nearest_loc:
                nearest_loc = my_num

            msg = f"Seed #{seed_count}".ljust(15)
            msg += f"[{seed + x}]".ljust(15) + " = "
            msg += f"[{my_num}]".ljust(15)
            msg += f"Nearest Location: {nearest_loc}".rjust(35)

            if old_nearest != nearest_loc:
                report["PART B"].append(msg)
                if len(report["PART B"]) > 30:
                    report["PART B"].pop(0)

                os.system("cls")
                print("PART A TESTS")
                for row in report["PART A"]:
                    print("\t", row)
                print("PART B TESTS")
                for row in report["PART B"]:
                    print("\t", row)
    return nearest_loc


###############################################################################
# ENTRY POINT FOR SUBMITTING & BENCHMARKING


def main(source=None):
    """entry point for aocd benchmarking,
    also: if running __main__ then we can
    force the data set here.
    """

    if source is None:
        source = open("input.txt").read()

    this_almanac = build_almanac(source)

    return (solve_a(this_almanac), solve_b(this_almanac))


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
    this_puzzle = aocd.models.Puzzle(year=2023, day=5, user=me)

    if not this_puzzle.answered_a:
        this_puzzle.answer_a = final_answer_a
    if not this_puzzle.answered_b:
        this_puzzle.answer_b = final_answer_b
