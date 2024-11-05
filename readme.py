"""

"""
import os

# import pickle
# import glob
# import configparser
# from sys import prefix

import datetime, time
import json
import aocd
import workspace
import toml 
from pathlib import Path

def cls():
    os.system("cls")

# puzzle standard format
readme_lines = json.loads(Path("templates/templates.json").read_text())
sections = ["header 1","aoc_portion","qaoc_portion","Header_events","Header_Year","day",]
# "named" 
#     "doc" : "templates/aoc.md",
#     "replacements" : ["{year}"]

cfg = toml.loads(Path(".env").read_text())

token = cfg["user"]["token"]  #.get("user", "token")
now = datetime.datetime.now()

# report_parts = dict(json.loads(open("readme.json").read()))
my_stats = workspace.Rankings(token)
report = []
cls()

# for year in range(2015, now.year + 1):
#     user_stats = aocd.models.User(token).get_stats(year)


def show_report():
    cls()
    print("\n".join(report))


def md_named(txt:str, data:dict)->str:
    for item, repl in data.items():
        txt = txt.replace(item, repl)

    show_report()
    return txt


def md_header(lvl:int, txt:str)->str:
    # header: ### [adventofcode.com/{year}](https://adventofcode.com/{year})
    prefix = ""
    if lvl > 1:
        prefix = "\n"

    show_report()
    return prefix + f"{'#' * lvl} {txt}".title() + "\n"


def std_day_report(year, day, day_data):
    # - {year} Day {day:02} [{solved_a}][{solved_b}] [{title}]
    # (https://adventofcode.com/{year}/day/{day})
    title = day_data["title"]
    part_a, part_b = day_data["parts"]
    # received from stats: [part, rank, points]
    _, ar, ap = part_a
    _, br, bp = part_b
    solved_a, solved_b = "_", "_"

    total_points = ap + bp

    if ar > 0:
        solved_a = "X"
    if br > 0:
        solved_b = "X"

    addend = ""
    if total_points > 0:
        addend = f" {total_points} Global Points!"

    new_line = f"- {year} Day {day:02} [{solved_a}][{solved_b}] [{title}]"
    new_line += f"(https://adventofcode.com/{year}/day/{day}){addend}"
    show_report()
    return new_line


###############################################################################
# BUILDING REPORT
###############################################################################
# Step 1: MAIN HEADER (level 1)
# static text from json storage

for item in sections:
    data = readme_lines[item]
    if item.lower().startswith("header"):
        lvl = data["lvl"]
        txt = data["txt"]
        report.append(md_header(lvl, txt))
    elif item == "day":
        

report.append(body)
show_report()


###############################################################################
# Step 2: CURRENT EVENT (level 2) {year}
# find latest event in stats
#   loop over all the puzzles in latest event,
#   format lines by event day ascending (Std Format)

show_report()
try:
    my_stats.pull_from_local(LATEST_EVENT)
except KeyError:
    my_stats.pull_year_from_aocd(LATEST_EVENT)

# loop the puzzles
for puzzle_day in my_stats[str(LATEST_EVENT)]:
    DAY_STATS = my_stats.get_day_stats(LATEST_EVENT, int(puzzle_day))
    ROW_TEXT = std_day_report(LATEST_EVENT, int(puzzle_day), DAY_STATS)
    report.append(ROW_TEXT)
    show_report()
    time.sleep(2)


###############################################################################
# Step 3: PREVIOUS EVENTS

# for each year, new Level 3 section
# header: ### [adventofcode.com/{year}](https://adventofcode.com/{year})
report.append(md_header(2, f"Previous events: 2015 - {LATEST_EVENT-1}"))


previous_years = [x for x in range(2015, LATEST_EVENT)]
previous_years.sort(reverse=True)
for p_year in previous_years:
    #   loop over all the puzzles in previous events,

    try:
        my_stats.pull_from_local(p_year)
        time.sleep(2)
        
    except:
        my_stats.pull_year_from_aocd(p_year)
        time.sleep(2)


    if str(p_year) in my_stats:
        ### [adventofcode.com/2022](https://adventofcode.com/2022)
        report.append(
            md_header(
                3, f"[adventofcode.com/({p_year})](https://adventofcode.com/{p_year})"
            )
        )

        open("Readme.md", "w").write("\n".join(report))

        # print(f"Days found in year: {p_year}: {my_stats[str(p_year)]}")

        days = [int(x) for x in my_stats[str(p_year)]]
        days.sort()

        #   format lines by event day ascending (Std Format)
        for p_day in days:
            DAY_STATS = my_stats.get_day_stats(p_year, int(p_day))
            ROW_TEXT = std_day_report(p_year, int(p_day), DAY_STATS)
            report.append(ROW_TEXT)
            show_report()

Path("Readme.md").write_text("\n".join(report))

# open("Readme.md", "w").write("\n".join(report))


###############################################################################
# Step 4: Footer text
# static from json storage


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# I WANT TO TRY A LINE BY LINE READ/REWRITE STYLE IF AT ALL POSSIBLE.
# MAYBE THAT WILL WORK SINCE THE "".replace() ISN'T DOING IT'S JOB.
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
