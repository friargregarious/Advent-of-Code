import argparse
from genericpath import exists
import pickle
import os, sys
import toml
import aocd
import requests
import markdownify

# from html.parser import HTMLParser
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime
from turtle import pu

config = toml.load('.env')


def year():
    return datetime.now().year


def month():
    return datetime.now().month


def day():
    return datetime.now().day


def example_text(puzzle):
    return puzzle.examples[0]


def solve_text(puzzle):
    return Path("solve_example.py").read_text()


def readme_text(puzzle:aocd.models.Puzzle, part:str="A"):
    # soup = BeautifulSoup(puzzle.prose0_path.read_text(encoding="utf-8"), "html.parser")
    # articles = [x.prettify() for x in soup.find_all("article")]
    # marked_down = markdownify.markdownify(articles[0], heading_style="ATX")

    # for index, article in enumerate(articles):
    #     Path(f".article_{index:02}.html").write_text(article)
    #     Path(f".markdwn_{index:02}.md").write_text(marked_down)

    
    soup = BeautifulSoup(puzzle._get_prose().encode("utf-8"), "html.parser")
    # soup = BeautifulSoup(puzzle.prose0_path.read_text(encoding="utf-8"), "html.parser")
    
    # puzzle._get_prose()
    
    articles = "\n".join( [str(x) for x in soup.find_all("article")])
    # articles.replace(r"\-\-\-" ,"---")
    md_articles = markdownify.markdownify(articles, heading_style="ATX")
    
    return md_articles


def build_defaults(target_path:Path, puzzle:aocd.models.Puzzle, part:str, y=None, d=None):
    _y = y if y else year()
    _d = d if d else day()
    
    if puzzle is None:
        puzzle = aocd.models.Puzzle(year=y, day=d)
    
    p_path = target_path / f"puzzle_{_y:04}_{_d:02}.aocd"
    with p_path.open("wb") as f:
        pickle.dump(puzzle, f)
        
    if part.upper() == "A":
        
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
                "content" : puzzle.input_data
                },
            
            }
    

    
        if not puzzle.input_data:
            files["INPUT"]["content"] = requests.get(puzzle.input_data_url).text
        else:
            files["INPUT"]["content"] = puzzle.input_data

    elif part.upper() == "B":

        PROSE = [
            ("Prose 0", puzzle.prose0_path),
            ("Prose 1", puzzle.prose1_path),
            ("Prose 2", puzzle.prose2_path),
            
        ]
        os.system("cls")
        for name, path in PROSE:
            if path.exists():
                print("*****************\n", name, path)
                # puzzle.prose2_
                print(path.read_text())
            
        sys.exit(0)
        
        files = {
            "README" : {
                "path" : target_path / f"README.md", 
                "content" : readme_text(puzzle)
                },
        }

    for _, v in files.items():
        if not v["path"].exists():
            v["path"].write_text(v["content"])
        
        if part.upper() == "B":
            v["path"].write_text(v["content"])
            

        
    # default_path = Path().parent / 'src'
    # for filename in default_path.iterdir():
    #     if filename.is_file():
    #         filename.rename(target_path / filename.name)
    
    
###############################################################################
# command line interface
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", help="Year of the puzzle to build.", type=int)
    parser.add_argument("--day", help="Day of the puzzle to build.", type=int)
    parser.add_argument("--part", help="Part of the puzzle to build. (A or B, default 'Part A').", type=str, default="A")

    args = parser.parse_args()

    _year = args.year if args.year else year()
    _day = args.day if args.day else day()

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

    build_defaults(y=_year, d=_day, target_path=day_to_build, puzzle=puzzle, part=args.part)
