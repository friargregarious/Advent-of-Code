# all tools used to solve puzzles

from aocd import cookies
from aocd.models import Puzzle, User
from aocd.exceptions import AocdError
from aocd.get import get_puzzle, get_leaderboard, get_leaderboard_private, get_leaderboard_public

import aocd




from math import e
from .solve_utilities import (
    Discord,
    INI_PARTS,
    Path,
    get_config,
    json,
    open_puzzle,
    os,
    refresh_readme,
    sys,
    toml,
    update_header,
)


token = None
t_errors = []
while token is None:
    # DO WE HAVE A WORKING TOKEN IN OUR ENVIRONMENT?
    if EnvironmentError not in t_errors:
        try:
            token = os.getenv("AOC_TOKEN")
        except Exception as e:
            token = None
            t_errors.append(e)

    # DID WE STORE A TOKEN IN OUR WORKING DIRECTORY?
    if FileExistsError not in t_errors:
        try:
            for file in Path(".").glob("*.env"):
                can_read = file.read_text(encoding="utf-8")

                token = Path(".token").read_text(encoding="utf-8")


            token = toml.loads(Path(".token").read_text(encoding="utf-8"))["Aoc"]["token"]
        except Exception as e:
            token = None
            t_errors.append(e)

    if AocdError not in t_errors:
        try:
            token = cookies.get_session_cookie()
        except Exception as e:
            token = None
            t_errors.append(e)

else:
    if token is not None:
        USER = aocd.models.User(token)
    else:
        USER = None


def get_config() -> dict:
    """
    Attempts to read a configuration dictionary from a file named '.env'.

    If the file does not exist, an empty dictionary is returned.

    Returns:
        A dictionary containing configuration data read from '.env'.
    """
    try:
        token = os.getenv("AOC_TOKEN")
    except EnvironmentError:
        token = Path("C:/dev/Advent of Code/.token").read_text(encoding="utf-8")

    if "AoC" in Path(__file__).as_posix():
        cfg_path = Path(__file__).parent.parent.parent.parent / ".env"
    else:
        cfg_path = Path(".env")

    return toml.loads(cfg_path.read_text(encoding="utf-8"))

ARGS_LIST = json.loads(Path("args.json").read_text(encoding="utf-8"))


def print_args(args: dict):
    """
    Prints the provided arguments in a formatted manner.

    Args:
        args (dict): A dictionary of arguments to be printed, where the keys are argument names
        and the values are their respective values.

    Effects:
        Prints a separator line, followed by the formatted argument names and values, and ends
        with another separator line.
    """
    width = 80
    bar = "*" * width
    print(" Args ".center(width, "*"))
    print(
        "\n".join(
            [
                f"{ k.replace('_', ' ').capitalize().rjust(10) } : { str(v).ljust(10) }".center(
                    width
                )
                for k, v in args.items()
            ]
        )
    )
    print(bar)


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")





clear_screen()

# Load puzzle parameters
INI = get_config()

# open puzzle info
PUZZLE = open_puzzle(INI)


def build_args_list(arguments: argparse.ArgumentParser):
    # Collect command line arguments
    args_path = Path(__file__).parent / "args.json"
    ARGS = json.loads(args_path.read_text())

    for arp, ark in ARGS_LIST:
        arguments.add_argument(*arp, **ark)

    args = vars(arguments.parse_args())

    # SHOW ARGUMENT SELECTIONS
    print_args(args)

    # DO IMMEDIATELY IF SELECTED
    if args.discord:
        Discord(puzzle=PUZZLE, config=INI)
        sys.exit()

    if args.refresh:
        refresh_readme(PUZZLE)
        sys.exit()

    #      DO_A             DO_B         DO_EXAMPLE    VERBOSE      SUBMIT
    return not args.part_b, args.part_b, args.example, args.verbose, args.submit


def get_DATA(is_example: bool):
    return "example_a.txt" if is_example else "input.txt"


def build_submit_msg(DO_A, DO_EXAMPLE, SUBMIT):

    msg = f"Doing {'A' if DO_A else 'B'}"
    msg += f" on {'example' if DO_EXAMPLE else 'input'}"
    msg += f" {'submit' if SUBMIT else 'localy'}"
    print(msg)


def do_submit(DO_A, PUZZLE, result):

    CORRECT_ANSWER = "unknown"
    if DO_A:
        if PUZZLE.answered_a:
            CORRECT_ANSWER = PUZZLE.answer_a

    else:
        if PUZZLE.answered_b:
            CORRECT_ANSWER = PUZZLE.answer_b

    compare = CORRECT_ANSWER == str(result)

    msg = f"Part {'A' if DO_A else 'B'}: {result}"
    msg += f" {result} == {CORRECT_ANSWER} [{compare}]"
    msg += f"IS {'NOT' if compare else ''} CORRECT!! ({CORRECT_ANSWER})"

    print(msg)

    update_header(PUZZLE)
    os.system("black .")


# tools actually called by solve file
__all__ = [
    os,
    toml,
    sys,
    Path,
    json,
    INI_PARTS,
    do_submit,
    print_args,
    get_DATA,
    clear_screen,
]
