import argparse
import platform
import sys
import toml
import aocd
import requests

from bs4 import BeautifulSoup
from markdownify import markdownify
from pathlib import Path
from datetime import datetime
try:
    from . import solve_utilities as su
except:
    import solve_utilities as su

config = su.get_config()


def year():
    """
    Returns the current year as a four-digit integer.

    Returns:
        int: The current year.
    """
    return datetime.now().year


def month():
    """
    Returns the current month as an integer.

    Returns:
        int: The current month.
    """
    return datetime.now().month


def day():
    """
    Returns the current day of the month as an integer.

    Returns:
        int: The current day of the month.
    """
    return datetime.now().day


def example_text(puzzle):
    """
    Returns the example text for the given puzzle.

    Args:
        puzzle (aocd.models.Puzzle): The puzzle object to return the example text for.

    Returns:
        str: The example text for the puzzle.
    """
    return puzzle.examples[0]


def solve_text(puzzle:aocd.models.Puzzle):
    """
    Generates a formatted header for a given Advent of Code puzzle and inserts it into a template file.

    Args:
        puzzle (aocd.models.Puzzle): The puzzle object containing metadata used to create the header.

    Returns:
        str: The text of the template file with the generated header inserted.
    """
    bar = "#" * 80
    blank = f"#{' ' * 78}#"

    a_done = "N/A"
    b_done = "N/A"
    day_done = datetime(year=puzzle.year, month=12, day=puzzle.day, hour=0, minute=0, second=0)
    if puzzle.answered_a:
        dt_a = day_done + puzzle.my_stats['a']['time']
        a_done = dt_a.strftime('%Y-%m-%d %H:%M')
    if puzzle.answered_b:
        dt_b = day_done + puzzle.my_stats['b']['time']        
        b_done = dt_b.strftime('%Y-%m-%d %H:%M')
        
    headers = [
        bar, blank,
        "#" + f"ADVENT OF CODE: {year()}".center(78) + "#",
        "#" + puzzle.title.center(78) + "#",
        "#" + puzzle.url.center(78) + "#",
        blank, bar,
        blank,
        "# A SOLVED:".ljust(14) + f"{a_done}".ljust(80-15) + "#",
        "# B SOLVED:".ljust(14) + f"{b_done}".ljust(80-15) + "#",
        "# SOLVER:".ljust(14) + "friargregarious (greg.denyes@gmail.com)".ljust(80-15) + "#",
        "# HOME:".ljust(14) + "https://github.com/friargregarious".ljust(80-15) + "#",
        blank,
        f"#" + f"WRITTEN AND TESTED IN PYTHON VER {platform.python_version()}".center(76) + "#",
        blank, bar               
        ]
    
    page = Path( "solve_example.py" ).read_text()
    page = page.replace( "{#HEADER}", "\n".join(headers) )
    
    return page


def readme_text(puzzle:aocd.models.Puzzle):
    """
    Gets the text of the puzzle page from adventofcode.com and
    translates it into markdown format using the markdownify library.

    Args:
        puzzle (aocd.models.Puzzle): The puzzle object to get the text from

    Returns:
        str: The markdown text of the puzzle page
    """
    
    soup = BeautifulSoup(puzzle._get_prose().encode("utf-8"), "html.parser")
    articles = "\n".join( [str(x) for x in soup.find_all("article")])
    md_articles = markdownify(articles, heading_style="ATX")
    md_articles = md_articles.replace( r"\-", "-" )
    
    return md_articles


def build_defaults(target_path:Path, puzzle:aocd.models.Puzzle, cfg:dict):
    _y = cfg["puzzle"]["year"] 
    _d = cfg["puzzle"]["day"]
    
    # user = aocd.get_user(cfg["user"]["token"])
    
    if puzzle is None:
        puzzle = su.open_puzzle(cfg) #  aocd.models.Puzzle(year=y, day=d, user=user)
    
    p_path = target_path / cfg["puzzle"]["path"]
    su.save_puzzle(puzzle, p_path)
        
    if not puzzle.answered_a or len(list(target_path.glob("*"))) == 0:
        
        files = {
            "EXAMPLE" : {
                "path" : target_path / f"example_a.txt",
                "content" : puzzle.examples[0].input_data
                },
            "SOLVE" : {
                "path" : target_path / f"Solve_{_y:04}_{_d:02}.py",
                "content" : solve_text(puzzle),
                },
            "README" : {
                "path" : target_path / f"README.md",
                "content" : readme_text(puzzle)
                },
            "INPUT" : {
                "path" : target_path / "input.txt",
                "content" : puzzle.input_data or requests.get(puzzle.input_data_url).text
                },
            "CFG" : {
                "path" : target_path / ".env",
                "content" : toml.dumps(cfg)
                },
            "utils" : {
                "path" : target_path / "solve_utilities.py",
                "content" : Path("solve_utilities.py").read_text()
            }
            }

        for _, v in files.items():
            if not v["path"].exists():
                v["path"].write_text(v["content"], encoding="utf-8")
            
    else:
        if puzzle.examples[1]:
            path = target_path / f"example_b.txt"
            path.write_text(puzzle.examples[1].input_data)

        elif puzzle.examples[2]:
            path = target_path / f"example_c.txt"
            path.write_text(puzzle.examples[2].input_data)
            
        path = target_path / f"README.md"
        content = readme_text(puzzle)
        path.write_text(content)
        
        
###############################################################################
# command line interface
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-y", "--year", help="Year of the puzzle to build.", type=int, default=year(), action="store")
    parser.add_argument("-d", "--day", help="Day of the puzzle to build.", type=int, default=day(), action="store")
    # parser.add_argument("-p", "--part", help="Part of the puzzle to build. (A or B, default 'Part A').", type=str, default="A", action="store")
    args = parser.parse_args()

    _year = args.year
    _day = args.day

    config = su.get_config()
    if len(config) == 0:
        print("No config file found. Please locate it and try again.")
        sys.exit(1)

    config['puzzle'] = { "year" : _year, "day" : _day, "path" : f"puzzle_{_year:04}_{_day:02}.aocd" }

    puzzle = aocd.models.Puzzle(
        year=_year, 
        day=_day, 
        user=aocd.models.User(config['user']['token'])
        )

    year_folder = f"AOC {_year:04}"
    day_folder = f"Day {_day:02}"

    year_to_build = Path().cwd().parent / year_folder
    if not year_to_build.exists():
        year_to_build.mkdir(parents=True)
    
    day_to_build = year_to_build / day_folder
    if not day_to_build.exists():
        day_to_build.mkdir(parents=True)

    su.save_config(config)
    build_defaults(cfg=config, target_path=day_to_build, puzzle=puzzle)
