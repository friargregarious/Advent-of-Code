"""# The almanac starts by listing which seeds need to be planted:"""
import os
from datetime import datetime

time_start = datetime.now()

os.system("cls")


def time_stamper(started_at, prefix):
    """for benchmarking"""
    # os.system("cls")
    time_difference = datetime.now() - started_at
    print(prefix.rjust(40), str(time_difference).ljust(15))


# raw = open("example.txt").read()
raw = open("input.txt").read()
# raw = open("small_example.txt").read()
seed_bag = []
to_process = {}
my_maps = {}

KEY = ""

for index, line in enumerate(raw.split("\n")):
    if len(line) >= 1:
        header_line = line[0].isalpha()
        number_line = line[0].isdigit()

        if header_line:
            if line.startswith("seeds: "):
                seed_bag = [int(x) for x in line.split(": ")[1].split()]
            else:
                header = line.strip(" map:\n").replace("-", "_")
                to_process[header] = []
                KEY = header

        if number_line:
            nums = [int(x) for x in line.split()]
            to_process[KEY].append(nums)


class grouping:
    """place holder"""

    def __init__(self):
        self._options = []

    def add_option(self, line):
        """
        stores tuple of digits to options
        """
        des, src, rng = [int(x) for x in line.split()]
        # three numbers:
        # the destination range start,
        #       the source range start,
        #               and the range length.
        # DES, SOURCE, RANGE
        # SOIL, SEED, RANGE
        new_option = (src, src + rng, des)

        self._options.append(new_option)

    def get_target(self, looking_for):
        """place holder"""
        for src_start, src_end, des in self._options:
            if src_start <= looking_for <= src_end:
                target_num = des + (looking_for - src_start)
            return target_num


# fill the almanac
def build_almanac_part_a(processing):
    """all the farmers come running to my yard"""

    a = {}
    headers = processing.keys()

    for head in headers:
        a[head] = {}
        for destination, source, ctr in to_process[head]:
            # That is, the section that starts with
            # seed-to-soil map: describes how to convert
            #       a seed number (the source) to
            #       a soil number (the destination)

            # three numbers:
            # the destination range start,
            #       the source range start,
            #               and the range length.
            # DES, SOURCE, RANGE
            # SOIL, SEED, RANGE
            temp = {source + x: destination + x for x in range(ctr)}
            a[head].update(temp)

    # for head in headers:
    #     report = []
    #     for line in processing[head]:
    #         DES, SRC, RNG = line
    #         msg = f"\n{head}: {line} translates to"
    #         msg += f" {SRC}:{DES} -> {SRC+RNG}:{DES+RNG}"
    #         report.append(msg)

    #     left, right = head.split("_to_")
    #     column_titles = f"\n{left} -> {right}\n"
    #     report.append(column_titles)
    #     for src, des in a[head].items():
    #         lk = str(src)
    #         rv = str(des)
    #         msg = f"{lk.center(len(left))} -> {rv.center(len(right))}\n"
    #         report.append(msg)

    #     open(f"{head}.txt", "w", encoding="utf-8").writelines(report)

    return a


def seed_to_location_part_a(alman, seed):
    """final output"""

    # finally, return the seed for the soil needed
    if seed in alman["seed_to_soil"]:
        soil = alman["seed_to_soil"][seed]
    else:
        soil = seed

    # fertilizer to soil
    if soil in alman["soil_to_fertilizer"]:
        fert = alman["soil_to_fertilizer"][soil]
    else:
        fert = soil

    # step 5 water to fertilizer
    if fert in alman["fertilizer_to_water"]:
        water = alman["fertilizer_to_water"][fert]
    else:
        water = fert

    # step 4 light to water
    if water in alman["water_to_light"]:
        lite = alman["water_to_light"][water]
    else:
        lite = water

    # step 3 temp to light
    if lite in alman["light_to_temperature"]:
        temp = alman["light_to_temperature"][lite]
    else:
        temp = lite

    # step 2 humidity to temp
    if temp in alman["temperature_to_humidity"]:
        humd = alman["temperature_to_humidity"][temp]
    else:
        humd = temp

    # step one, location to humidity
    if humd in alman["humidity_to_location"]:
        loc = alman["humidity_to_location"][humd]
    else:
        loc = humd

    return (seed, soil, fert, water, lite, temp, humd, loc)


my_almanac = build_almanac_part_a(to_process)

for seed in seed_bag:
    print(seed_to_location_part_a(my_almanac, seed))
