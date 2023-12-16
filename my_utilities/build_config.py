import os
import sys
import configparser
from datetime import datetime
import aocd

arg_keys = sys.argv[1:]
arg_dict = {x.lower(): y for x, y in zip(arg_keys[0::2], sys.argv[1::2])}



if "-y" in arg_dict:
    year = int(arg_dict["-y"])
else:
    year = aocd.get.most_recent_year()

if "-d" in arg_dict:
    day = int(arg_dict["-d"])
else:
    day = aocd.get.current_day()

if year, day

# protect from future grabing puzzles
p = aocd.get_puzzle(year, day)


# if "-e" in arg_dict:
#     EXAMPLE = True
#     correct_example_a, correct_example_b = arg_dict["-e"].split(",")
# else:
#     EXAMPLE = False
#     correct_example_a, correct_example_b = None, None

my_date_stamp = f"{year}-{day}"
config_to_write = ".env"


###############################################################################
# HELPER FUNCTIONS ############################################################

def pad(d:int)->str:
    return str(d).rjust(2, "0")


def new_path(y: int, d: int) -> str:
    """generates a new path string"""
    return f"../AOC {y}/Day {pad(d)}/"


def move_old_ini(date_stamp):
    # first, we don't want to overwrite an old file, we'll just
    # move and rename the old one before writing the new one.
    try:
        src = config_to_write
        dst = config_to_write[:-4] + date_stamp + ".ini"
        dst_dir = "../.unused"
        os.rename(src=src, dst=dst, dst_dir_fd=dst_dir)
        return os.path.isfile(dst_dir + dst) and not os.path.isfile(src)
    except FileExistsError as fe:
        msg = [f"The file {dst} already exists in {dst_dir}"]
        msg.extend([k for k in list(fe.items())])
        sys.exit("\n".join(msg))


# eventually I will code a method for pulling
# AoC user name and token information to store it here
# also leaderboard options and files to manage during
# new_day and update_readme executions.


###############################################################################
# MAIN BUILD PORTION ##########################################################
def main(y: int, d: int):
    """only runs if executed from console"""
    config = configparser.ConfigParser()

    config["user"] = {
        "user_name": "FriarGregarious",
        "token": "53616c7465645f5fb0cb736de70d93a2932ed7b03dfac8d4294c83b64cfc22eeb70d7cdf944f7b61cbfd7ce223d4a12165bbfb9057b949f8f143959d6c7b551a",
    }

    config["leaderboard"] = {
        "AOC_JOIN_PRIVATE_LEADERBOARDS": "2588518-0a9244b0",
        "address": "https://adventofcode.com/2023/leaderboard/private/view/2588518",
        "json": "https://adventofcode.com/2023/leaderboard/private/view/2588518.json",
        "json_file": "leader_board.json",
    }

    file_names = [
        "solve": f"Solve_{y}_{pad(d)}.py",
        "inst": "readme.md",
        "input": "input.txt",
        "example": "example.txt",
        "license": "license.txt",
        "utils": "my_utils.py",
        "setup": "setup.py",
        ]

    config["new_day"] = {"default_path": "../default/","new_path": new_path(year, day)}
    for fn in file_names:
        config["new_day"][f"default_{fn}"] = "../default/"+fn
    for fn in file_names:
        config["new_day"][f"new_{fn}"] = new_path(year, day) + fn

    try:
        # first, we don't want to overwrite an old file, we'll just
        # move and rename the old one before writing the new one.
        if os.path.isfile(config_to_write):
            move_old_ini(my_date_stamp)

        with open(config_to_write, "w", encoding="utf-8") as cfgfile:
            config.write(cfgfile)

        if os.path.isfile(config_to_write):
            sys.exit(0)
        else:
            msg = f"Config File {config_to_write} created successfully!"

    except Exception as e:
        msg = e

    sys.exit(msg)


if __name__ == "__main__":
    main(year, day)
