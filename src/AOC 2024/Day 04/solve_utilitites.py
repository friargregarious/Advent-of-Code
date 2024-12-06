from genericpath import isfile
import aocd
import pickle
import time
import sys
from numpy import save
import requests
import toml

from markdownify import markdownify
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime


def print_args(args:dict):
    bar = "*" * 50
    print( bar, f"{' Args ':*^50}", bar, sep="\n" )

    for param in [ f"{ k.rjust(12) }: { v }" for k, v in args.items() ]:
        print("-->", param)

    print( bar )


def get_user_results(user:aocd.models.User):
    this_year = datetime.now().year
    possible_years = [2015 + x for x in range(this_year - 2015)]
    user_stats = user.get_stats(years=possible_years)
    return user_stats

def save_config(config:dict):
    try:
        Path(".env").write_text(toml.dumps(config))
        print("RESULT: Save Config: .env")
    except:
        print("RESULT: Failed to save Config: .env")
        sys.exit(0)

def save_puzzle(puzzle: aocd.models.Puzzle, path:Path):
    try:
        pickle.dump(puzzle, open(path, "wb"))
        print("RESULT: Saved Puzzle: " + str(path))
    except:
        print("RESULT: Failed to save Puzzle: " + str(path))

def open_puzzle(config:dict):
    _puzzle_path = Path(config['puzzle']['path'])
    _year = config['puzzle']['year']
    _day = config['puzzle']['day']
    _user = aocd.models.User(config['user']['token'])

    def net_get():
        puzzle = aocd.models.Puzzle( year=_year, day=_day, user=_user )
        print(f"Creating new puzzle file: {_puzzle_path}")
        save_puzzle(puzzle, _puzzle_path)
        return puzzle
        
    if Path(config['puzzle']['path']).is_file():
        try:
            puzzle = pickle.load(open(_puzzle_path, "rb"))
            puzzle._user = _user
            print( f"Found existing puzzle file: {_puzzle_path}" )
            return puzzle
        except:
            print( f"Existing File Corrupted: {_puzzle_path}" )
            return net_get()

    else:
        print( f"No puzzle file found: {_puzzle_path}" )
        return net_get()


def refresh_readme(puzzle:aocd.models.Puzzle):
    try:
        puzzle._request_puzzle_page()
        soup = BeautifulSoup( puzzle._get_prose().encode("utf-8"), "html.parser" )
        articles = "\n".join( [str(x) for x in soup.find_all("article")] )
        articles = articles.replace( r"\-" ,"-" )
        md_articles = markdownify( articles, heading_style="ATX" )
        Path( "README.md" ).write_text( md_articles )
        print( "RESULT: Refreshed README.md" )
    except:
        print( "RESULT: Failed to refresh README.md" )
    sys.exit(0)


def submit_result(puzzle: aocd.models.Puzzle, result:int, part:str, path:Path):    
    """
    Submits the result of a puzzle to AoC servers.

    Args:
        puzzle: the puzzle object to submit the result to
        result: the result of the puzzle to submit
        part: which part of the puzzle to submit (A or B)
        path: the path to save the puzzle object after submitting

    Effects:
        Submits the result to AoC servers and saves the updated puzzle object
    """
    time.sleep(3)

    if part.upper() == "A" and not puzzle.answered_a:
        puzzle.answer_a = result # type: ignore
        if puzzle.answered_a:
            save_puzzle(puzzle, path)
            
    elif part.upper() == "B" and not puzzle.answered_b:
        puzzle.answer_b = result # type: ignore
        if puzzle.answered_b:
            save_puzzle(puzzle, path)


def report_puzzle(puzzle: aocd.models.Puzzle, result:int, part:str):
    """
    Reports the result of the puzzle to the console.

    Args:
        puzzle: the puzzle object
        result: the result of the puzzle
        part: which part of the puzzle to report (A or B)

    Effects:
        Prints the result of the puzzle to the console
    """

    if part.upper() == "A":
        if puzzle.answered_a: print(f"Part A is completed: {puzzle.answer_a}")
        else: print( "Part A:", result, "(Completed)")

    elif part.upper() == "B":
        if puzzle.answered_b: print(f"Part B is completed: {puzzle.answer_b}")
        else: print( "Part B:", result, "(Completed)")


def Discord(config:dict, puzzle:aocd.models.Puzzle):
    """
    Posts a message to the specified Discord channel to gloat about
    completing both parts of the puzzle.

    Args:
        config: the configuration dictionary
        puzzle: the puzzle object

    Effects:
        Posts a message to the Discord channel and saves the configuration
        with last_msg set to True.

    Returns:
        None
    """
    _year = config['puzzle']["year"]
    _day = config['puzzle']["day"]
    _general = config['discord']['general']
    _token = config['discord']['token']
    
    if config['discord']['last_msg']:
        print("RESULT: You have already posted your message to discord.")

    elif puzzle.answered_a and puzzle.answered_b:
        url = f"https://discord.com/api/v9/channels/{_general}/messages"

        msg = "Hey @everyone!!!\n"
        msg += f"I have completed AoC {_year} Day {_day:02}: "
        msg += f"**{puzzle.title}** Parts A & B\n{puzzle.url}"

        content = {"content": msg, "mention_everyone": True}
        header = {"Authorization": _token}

        res = requests.post(url, data=content, headers=header )
        
        if res.status_code != 200:
            print("RESULT: Discord Message Failed!")

        elif res.status_code == 200:
            print("RESULT: Discord Message Sent!")
            config['discord']['last_msg'] = True
            save_config(config)

    else:
        print("RESULT: You have not yet completed both parts of the puzzle.\nNo gloating till you're finished!")
        
    sys.exit(0)