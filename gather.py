import aocd
import argparse
import os, sys
import json, toml, pickle
import time
from datetime import datetime
from pathlib import Path

cfg = toml.loads(Path(".env").read_text(encoding="utf-8"))

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
    all_puzzles_path = Path(".puzzles")
    stats = USER.get_stats(years=[year])
    d_key = f"{year}/{day:02}"
    day_path = all_puzzles_path / f"{year}-{day:02}.aocd"

    if day_path.exists():
        try:
            p: aocd.models.Puzzle = pickle.loads(day_path.read_bytes())
            p._user = USER
            p._request_puzzle_page()
        except:
            p = aocd.models.Puzzle(year, day, USER)
    else:
        p = aocd.models.Puzzle(year, day, USER)

    pickle.dump(p, day_path.open("wb"))

    CORE[year][day] = {
        "title": p.title, 
        "url": p.url, 
        "results": {"A": "N/A", "B": "N/A"}, 
        }
                
    if d_key in stats:
        for part in stats[d_key]:
            if stats[d_key][part]['time'].days >= 1:
                CORE[year][day]["results"][part.upper()] = "24+ hours"
            
            else:
                hrs = stats[d_key][part]['time'].total_seconds() // 3600
                mins = stats[d_key][part]['time'].total_seconds() % 3600 // 60
                CORE[year][day]["results"][part.upper()] = f"{int(hrs):02} hours, {int(mins):02} minutes"

    Path("core.json").write_text(json.dumps(CORE, indent=3), encoding="utf-8")
                

def get_stats(year:int, day:int) -> dict:
    return CORE[year][day]
    

def generate_readme() -> str:            

    report = [
        "# Advent Of Code\n",
        Path("templates/aoc.md").read_text(encoding="utf-8").format(year=NOW.year),
        # Path("templates/qaoc.md").read_text(encoding="utf-8").format(year=NOW.year),        
    ]
    
    for year in sorted(CORE.keys(), reverse=True):
        if int(year) == NOW.year:
            year_line = f"\n## Current Event: {year} - <https://adventofcode.com/{year}>\n"
        else:
            year_line = f"\n## Previous AoC Event: {year} - <https://adventofcode.com/{year}>\n"
        
        report.append(year_line)

        unfinished_days = []
        for day in sorted(CORE[year].keys(), reverse=False):
            title = CORE[year][day]["title"]
            url = CORE[year][day]["url"]
            a = "X" if CORE[year][day]["results"]["A"] != "N/A" else "_"
            b = "X" if CORE[year][day]["results"]["B"] != "N/A" else "_"

            if not a == b == "_":
                day_line = f"- Day {int(day):02} [{a}][{b}] [{title}]({url})"
                report.append(day_line)
            else:
                day_line = f"Day {int(day):02} [{title}]({url})"
                unfinished_days.append(day_line)

        if len(unfinished_days) > 0:
            unfinished_text = f"\n**Unfinished:** {", ".join(unfinished_days)}\n"
            report.append(unfinished_text)

    page = "\n".join(report)
    Path("README.md").write_text(page, encoding="utf-8")
    # print(page)
    # return page

    
if __name__ == "__main__":
    os.system("cls")

    NOW = datetime.now()
    YEARS = [ 2015 + x for x in range(NOW.year - 2015) ]
    USER = aocd.models.User(cfg["user"]["token"])
    CORE = json.loads( Path(cfg["working_dirs"]["core"]).read_text(encoding="utf-8") )

    args = argparse.ArgumentParser()
    args.add_argument("-g","--generate", help="Generate the readme text.", default=False, action="store_true")
    args.add_argument("-r","--refresh", help="Refresh the leaderboard data.", default=False, action="store_true")
    # args.add_argument("-y","--year", help=f"Year of the puzzle to build. (current: {NOW.year})", type=int, default=NOW.year)
    # args.add_argument("-d","--day", help=f"Day of the puzzle to build. (current: {NOW.year})", type=int, default=NOW.year)
    args = args.parse_args()
    print("Args:", ", ".join( [ f"{k} = {v}" for k,v in vars(args).items()] ) )
    
    if args.generate:
        generate_readme()
    
    # if args.refresh:
        # refresh_core(args.year, args.day, CORE)
        