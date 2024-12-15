import aocd
import argparse
import os, sys
import json, toml, pickle
import time
from datetime import date, datetime
from pathlib import Path

import build_days
from templates import solve_utilities as su


cfg = toml.loads(Path(".env").read_text(encoding="utf-8"))
cfg["working_dirs"]["templates"] = ["aoc.md", "qaoc.md",]
Path(".env").write_text(toml.dumps(cfg), encoding="utf-8")

def refresh_core(year:int, day:int, CORE:dict) -> None:

    """
    Refreshes the core data for a specific year and day.

    This function updates the `CORE` dictionary with the latest puzzle information
    and results for the specified `year` and `day`. It retrieves puzzle data from 
    the Advent of Code API using the `aocd` library, storing the data locally in 
    a pickle file. If the puzzle data already exists locally, it attempts to load 
    it; otherwise, it fetches it from the API.

    The function also updates the `CORE` dictionary with the puzzle's title, URL, and 
    results. It writes the updated `CORE` data back to the `core.json` file.

    Args:
        year (int): The year of the puzzle to refresh.
        day (int): The day of the puzzle to refresh.
        CORE (dict): The dictionary containing core puzzle data to be updated.

    Returns:
        None
    """
    # try:
    all_puzzles_path = Path(".puzzles")
    stats = USER.get_stats(years=year)
    d_key = f"{year}/{day:02}"
    day_path = all_puzzles_path / f"{year:04}-{day:02}.aocd"

    if day_path.exists():
        try:
            p: aocd.models.Puzzle = pickle.loads(day_path.read_bytes())
            p._user = USER
            # p._request_puzzle_page()
        except:
            p = aocd.models.Puzzle(year=year, day=day, user=USER)
    else:
        p = aocd.models.Puzzle(year=year, day=day, user=USER)
    
    _y, _d = f"{year:04}", f"{day:02}"
    
    CORE[_y][_d] = {
        "title": p.title, 
        "url": p.url, 
        "results": {"A": "N/A", "B": "N/A"}, 
        }
                
    if d_key in stats:
        for part in stats[d_key]:
            if stats[d_key][part]['time'].days >= 1:
                CORE[_y][_d]["results"][part.upper()] = "24+ hours"
            
            else:
                hrs = stats[d_key][part]['time'].total_seconds() // 3600
                mins = stats[d_key][part]['time'].total_seconds() % 3600 // 60
                CORE[_y][_d]["results"][part.upper()] = f"{int(hrs):02} hours, {int(mins):02} minutes"

    Path("core.json").write_text(json.dumps(CORE, indent=3, sort_keys=True ), encoding="utf-8")
    pickle.dump(p, day_path.open("wb"))



def get_stats(year:int, day:int) -> dict:
    _y, _d = str(year), str(day)    
    return CORE[_y][_d]
    

def generate_readme():

    report = [
        "# Advent Of Code\n",
        Path("templates/aoc.md").read_text(encoding="utf-8").format(year=NOW.year),
        # Path("templates/qaoc.md").read_text(encoding="utf-8").format(year=NOW.year),        
    ]

    # happy = 😁 😎 🧔🏼‍♂️         ♻️ 🆘  🔜 

 
     
    for year in sorted(CORE.keys(), reverse=True):
        if int(year) == NOW.year:
            year_line = f"\n## 🎈💃🏼 Current Event: {year} - <https://adventofcode.com/{year}> 🕺🏼🎉\n"
        else:
            year_line = f"\n## Previous AoC Event: {year} - <https://adventofcode.com/{year}>\n"
        
        report.append(year_line)

        unfinished_days = []
        for day in sorted(CORE[year].keys(), reverse=False):
            title = CORE[year][day]["title"]
            url = CORE[year][day]["url"]
            #   
            if CORE[year][day]["results"]["A"] == "24+ hours":
                a = "⌛"

            elif CORE[year][day]["results"]["A"] == "N/A":
                a = "😴"

            elif int(CORE[year][day]["results"]["A"].split(" hours")[0]) <= 12:   #"0 hours, 0 minutes":
                a = "😎"
            
            elif int(CORE[year][day]["results"]["A"].split(" hours")[0]) >= 12:
                a = "🤬"
                        


            if CORE[year][day]["results"]["B"] == "24+ hours":
                b = "⌛"

            elif CORE[year][day]["results"]["B"] == "N/A":
                b = "😴"

            elif int(CORE[year][day]["results"]["B"].split(" hours")[0]) <= 12:   #"0 hours, 0 minutes":
                b = "😎"
            
            elif int(CORE[year][day]["results"]["B"].split(" hours")[0]) >= 12:
                b = "🤬"


            if not a == b == "😴": # type: ignore
                day_line = f"- Day {int(day):02} [{a}][{b}] [{title}]({url})"
                report.append(day_line)
            else:
                day_line = f"Day {int(day):02} [{title}]({url})"
                unfinished_days.append(day_line)

        if len(unfinished_days) > 0:
            unfinished_text = f"\n☢️ **Unfinished:** ☣️ {", ".join(unfinished_days)} \n"
            report.append(unfinished_text)

    page = "\n".join(report)
    page = page.replace(" \n", "\n")
    page = page.replace("  ", " ")
    page = page.replace("\n\n\n", "\n\n")
    
    
    Path("README.md").write_text(page, encoding="utf-8")
    # print(page)
    # return page


def auto_load():
    global CORE
    CORE = json.loads( Path(cfg["working_dirs"]["core"]).read_text(encoding="utf-8") )

    year = max( map(int,  CORE.keys()) )
    target_day = max( map(int,  CORE[str(year)].keys()) ) + 1
    print(f"\n{' AUTO '.center(60, '-')}\n")
    while True:
        os.system("cls")
        now = datetime.now()
        time.sleep(90)
        print(f"AUTO: Waiting... {now.strftime('%Y-%m-%d %H:%M:%S')}")
        if now > datetime(year=year, month=12, day=target_day):
            try:
                print(f"building puzzle for {year} {target_day}")
                os.system(f"Advent.py -b -d={target_day}")
                print(f"Successfully built puzzle templates for {year} {target_day}")
                sys.exit(0)
            except:
                print(f"failed to build puzzle for {year} {target_day}")
                sys.exit(1)


    
if __name__ == "__main__":
    os.system("cls")

    NOW = datetime.now()
    YEARS = [ 2015 + x for x in range(NOW.year - 2015) ]
    USER = aocd.models.User(cfg["user"]["token"])
    CORE = json.loads( Path(cfg["working_dirs"]["core"]).read_text(encoding="utf-8") )

    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--generate", help="Generate the readme text.", default=False, action="store_true")
    parser.add_argument("-r", "--refresh", help="Refresh the leaderboard data.", default=False, action="store_true")
    parser.add_argument("-b", "--build", help="Build a new puzzle folder.", default=False, action="store_true")
    parser.add_argument("-y", "--year", help=f"Year of the puzzle to build (default {NOW.year}).", type=int, default=NOW.year, action="store")
    parser.add_argument("-d", "--day", help=f"Day of the puzzle to build (default {NOW.day}).", type=int, default=NOW.day, action="store")
    parser.add_argument("-a", "--auto", help=f"Time loop waiting for next day's puzzle to activate (default False).", default=False, action="store_true")
    
    args = vars( parser.parse_args() )
    su.print_args(args=args)

    cfg = toml.loads(Path(".env").read_text(encoding="utf-8"))
    
    # print("Args:", ", ".join( [ f"{k} = {v}" for k, v in args.items() ] ) )
        
    if args["build"]:
        cfg["puzzle"] = {
            "year": args["year"], 
            "day": args["day"],
            "path" : (Path(cfg["working_dirs"]["puzzles"]) / f"{args['year']:04}_{args['day']:02}.aocd").as_posix()
            }

        build_days.build_puzzle( cfg )
    
    if args["refresh"]:
        refresh_core(args["year"], args["day"], CORE)
        
    if args["generate"]:
        generate_readme()
    
    if args["auto"]:
        auto_load()

