"""# The almanac starts by listing which seeds need to be planted:"""
import os
from configparser import ConfigParser
import aocd


class Almanac(dict):
    """place holder"""

    seed_bag = []

    @property
    def nearest_location(self):
        nearest_loc = 9999999999999999999999

        answers = {x: [] for x in self.seed_bag}
        for seed in self.seed_bag:
            my_num = seed
            # print("Seed:", seed, end=", ")
            for layer in groups:
                my_num = self[layer].get_target(my_num)
                answers[seed].append(my_num)
                # print(layer.split("_to_")[1] + ":", my_num, end=", ")
            # print()
            if answers[seed][-1] < nearest_loc:
                nearest_loc = answers[seed][-1]
        return nearest_loc


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


def build_almanac(data_name):
    """placeholder"""
    raw = open(data_name, encoding="utf-8").read()
    this_almanac = Almanac()

    header_key = ""
    for line in raw.split("\n"):
        if len(line) >= 1:
            header_line = line[0].isalpha()
            number_line = line[0].isdigit()

            if header_line:
                if line.startswith("seeds: "):
                    this_almanac.seed_bag = [
                        int(x) for x in line.split(": ")[1].split()
                    ]
                else:
                    header = line.strip(" map:\n").replace("-", "_")
                    this_almanac[header] = Grouping()
                    header_key = header

                    if header_key:
                        pass

            if number_line:
                nums = [int(x) for x in line.split()]
                this_almanac[header].add_option(nums)

    return this_almanac

    # return (seed, soil, fert, water, lite, temp, humd, loc)


# for seed in seed_bag:
#     print(seed_to_location_part_a(my_almanac, seed))


if __name__ == "__main__":
    os.system("cls")
    # data_file_name = "example.txt"
    data_file_name = "input.txt"

    my_almanac = build_almanac(data_file_name)
    # for item in my_almanac.seed_bag:
    #     print(item, my_almanac["seed_to_soil"].get_target(item))

    groups = [
        "seed_to_soil",
        "soil_to_fertilizer",
        "fertilizer_to_water",
        "water_to_light",
        "light_to_temperature",
        "temperature_to_humidity",
        "humidity_to_location",
    ]

    nearest_loc = 9999999999999999999999999
    answers = {x: [] for x in my_almanac.seed_bag}
    for seed in my_almanac.seed_bag:
        my_num = seed
        # print("Seed:", seed, end=", ")
        for layer in groups:
            my_num = my_almanac[layer].get_target(my_num)
            answers[seed].append(my_num)
    for k, v in answers.items():
        print(k, v)

    print(f"nearest_location is {my_almanac.nearest_location}")


    final_answer_a = my_almanac.nearest_location



    cfg = ConfigParser()
    cfg.read("C:/Advent of Code/.env")
    token = cfg.get(section="friargregarious", option="token")
    me = aocd.models.User(token=token)
    this_puzzle = aocd.models.Puzzle(year=2023, day=5, user=me)
    this_puzzle.answer_a = final_answer_a

