"""

"""
import os
from datetime import datetime
import pickle
import glob
import configparser
import aocd
import aoc_to_markdown
from .unused import utils

# Get the directory name of the current executable
executable_path = os.path.dirname(os.path.abspath(__file__))
print(executable_path)

cfg = utils.get_cfg()


os.system("cls")
existing_puzzle_data = {x + 1: y for x, y in enumerate(glob.glob("*Puzzle.aocd"))}
# this_user = pickle.load(open("me.aocd"))

msg = "Please either select one of the existing puzzle files from the list \n"
msg += "or leave selection blank to pull today's puzzle data.\n"

print()
for index, filename in existing_puzzle_data.items():
    print(f"   {index}:  {filename}")

selection = input("\n your Selection: > ")

if selection.isdigit() and (0 < int(selection) <= len(existing_puzzle_data)):
    index = int(selection)
    working_puzzle = pickle.load(open(existing_puzzle_data[index]))
    year = working_puzzle.year
    day = working_puzzle.day

else:
    year = datetime.now().year
    day = datetime.now().day
    working_puzzle = aocd.models.Puzzle(year, day, user=this_user)


results = (working_puzzle.answered("a"), working_puzzle.answered("b"))
print("Results:", results)

day_title = working_puzzle.title
print(f"Puzzle Title: {day_title}")

url = f"https://adventofcode.com/{year}/day/{day}"
print("URL:", url)

day_anchor = "<!-- ENTER NEW DAY HERE  -->"
pad_day = str(day).rjust(2, "0")


def res_text(puzzle_results):
    """quickly format markdown from results"""
    output_string = ""
    for result in puzzle_results:
        if result:
            output_string += "[X]"
        else:
            output_string += "[_]"
    return output_string


NDM = "<!-- ENTER NEW DAY HERE -->"
new_day_text = f"- {year} Day {pad_day} {res_text(results)}"
new_day_text += f" [{day_title}]({url})\n{NDM}\n"

print(new_day_text)
readme = open("readme.md", "r", encoding="UTF-8").read()
open("test_before.txt", "w").write(readme)

readme.replace(NDM, new_day_text)


open("test_after.txt", "w").write(readme)


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# I WANT TO TRY A LINE BY LINE READ/REWRITE STYLE IF AT ALL POSSIBLE.
# MAYBE THAT WILL WORK SINCE THE "".replace() ISN'T DOING IT'S JOB.
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


# print(readme)

# new_day_text = "" + "\n"
# readme.replace(day_anchor, new_day_text+day_anchor)


# <!-- REPLACE DAYS BEGIN -->
# <!-- REPLACE DAYS END -->
