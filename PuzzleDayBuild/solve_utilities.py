import aocd
import pickle
import time
import sys
import requests
import toml

from markdownify import markdownify
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime


def print_args(args:dict):
    """
    Prints the provided arguments in a formatted manner.

    Args:
        args (dict): A dictionary of arguments to be printed, where the keys are argument names
        and the values are their respective values.

    Effects:
        Prints a separator line, followed by the formatted argument names and values, and ends
        with another separator line.
    """
    bar = "*" * 50
    print( bar, f"{' Args ':*^50}", bar, sep="\n" )

    for param in [ f"{ k.rjust(12) }: { v }" for k, v in args.items() ]:
        print("-->", param)

    print( bar )


def get_user_results(user:aocd.models.User):
    """
    Retrieves user statistics for the current year from the Advent of Code servers.

    Args:
        user (aocd.models.User): The user object for which to retrieve statistics.

    Returns:
        dict: A dictionary containing user statistics for the current year.
    """
    user_stats = user.get_stats(years=[datetime.now().year])
    return user_stats


def get_config()->dict:
    """
    Attempts to read a configuration dictionary from a file named '.env'.

    If the file does not exist, an empty dictionary is returned.

    Returns:
        A dictionary containing configuration data read from '.env'.
    """
    cfg_path = Path(".env")
    if cfg_path.is_file():
        return toml.loads( cfg_path.read_text(encoding="utf-8") )

    return {}
    

def save_config(config:dict):
    """
    Saves the given configuration dictionary to a file named '.env'.

    Args:
        config: A dictionary containing configuration data to be saved.

    Effects:
        Attempts to write the configuration data in TOML format to the '.env' file.
        Prints a success message if the file is saved successfully.
        Prints a failure message and exits the program if the save operation fails.
    """
    try:
        Path(".env").write_text(toml.dumps(config))
        print("RESULT: Save Config: .env")
    except:
        print("RESULT: Failed to save Config: .env")
        sys.exit(0)


def save_puzzle(puzzle: aocd.models.Puzzle, path:Path):
    """
    Saves a puzzle object to a file on disk.

    Args:
        puzzle: the puzzle object to save
        path: the path to save the puzzle object to

    Effects:
        Saves the puzzle object to disk and prints a message indicating success or failure
    """
    try:
        pickle.dump(puzzle, open(path, "wb"))
        print("RESULT: Saved Puzzle: " + str(path))
    except:
        print("RESULT: Failed to save Puzzle: " + str(path))


def open_puzzle(config:dict):
    """
    Opens a puzzle file. If the file does not exist, it is created from the AoC servers.
    If the file exists but is corrupted, it is deleted and recreated from the AoC servers.
    Otherwise, the existing file is loaded and returned.

    Args:
        config (dict): A dictionary with information about the puzzle to be opened.

    Returns:
        Puzzle: The opened puzzle object.
    """
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
    """
    Refreshes the README.md file with the latest puzzle text

    Args:
        puzzle: the puzzle object to get the text from

    Effects:
        Updates the README.md file and prints a success/failure message
    """
    try:
        puzzle._request_puzzle_page()
        soup = BeautifulSoup( puzzle._get_prose().encode("utf-8"), "html.parser" )
        articles = "\n".join( [ str(x) for x in soup.find_all("article") ] )
        md_articles = markdownify( articles )
        md_articles = md_articles.replace( r"\-" ,"-" )
        md_articles = md_articles.replace( r"\.", "." )
        md_articles = md_articles.replace("## --- Day", "# --- Day")
        file = Path( "README.md" )
        # import os
        # os.remove(file)
        file.write_text(md_articles, encoding="utf-8")
        # print( md_articles )
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
            update_header(puzzle)
            
    elif part.upper() == "B" and not puzzle.answered_b:
        puzzle.answer_b = result # type: ignore
        if puzzle.answered_b:
            save_puzzle(puzzle, path)
            update_header(puzzle)


def report_puzzle(puzzle: aocd.models.Puzzle, result, part:str):
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
    _token = config['discord']['token']
    
    if config['discord']['last_msg']:
        print("RESULT: You have already posted your message to discord.")
        print("This msg and following msgs will go to testing channel.")
        channel = config['discord']['testing']
    else:
        channel = config['discord']['general']


    if puzzle.answered_a and puzzle.answered_b:
        day_done = datetime(year=puzzle.year, month=12, day=puzzle.day, hour=0, minute=0, second=0)
        dta = day_done + puzzle.my_stats['a']['time']
        dtb = day_done + puzzle.my_stats['b']['time']

        # done = dt.strftime('%Y-%m-%d %H:%M')
        # new_text.append( "# A SOLVED:".ljust(14) + f"{done}".ljust(80-15) + "#" )
        
        url = f"https://discord.com/api/v9/channels/{channel}/messages"

        msg = "Hey @everyone!!!\n"
        msg += f"I have completed AoC {_year} Day {_day:02}: **{puzzle.title}**"
        msg += f"\n{puzzle.url}"
        msg += f"\n**Part A: {dta.strftime('%Y-%m-%d %H:%M')}**"
        msg += f"\n**Part B: {dtb.strftime('%Y-%m-%d %H:%M')}**"

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
    
def update_header(puzzle: aocd.models.Puzzle):
    """
    Updates the header of the solve file with the date the puzzle was solved
    for parts A and B. If the puzzle has not been solved yet, it leaves the
    header unchanged.

    Parameters:
        puzzle (aocd.models.Puzzle): The AoC puzzle object

    Returns:
        None
    """
    solve_file = Path( f"Solve_{puzzle.year:04}_{puzzle.day:02}.py" )

    if solve_file.exists():
        text = solve_file.read_text().split("\n")

    new_text = []

    day_done = datetime(year=puzzle.year, month=12, day=puzzle.day, hour=0, minute=0, second=0)

    for line in text:
        if line.startswith("# A SOLVED:"):
            if puzzle.answered_a:
                dt = day_done + puzzle.my_stats['a']['time']
                done = dt.strftime('%Y-%m-%d %H:%M')
                new_text.append( "# A SOLVED:".ljust(14) + f"{done}".ljust(80-15) + "#" )

        elif line.startswith("# B SOLVED:"):
            if puzzle.answered_b:
                dt = day_done + puzzle.my_stats['b']['time']
                done = dt.strftime('%Y-%m-%d %H:%M')
                new_text.append( "# B SOLVED:".ljust(14) + f"{done}".ljust(80-15) + "#" )

        else:
            new_text.append(line)

    solve_file.write_text("\n".join(new_text), encoding="utf-8")

# if __name__ == "__main__":
#     config = get_config()
#     puzzle = open_puzzle(config)
#     update_header(puzzle)