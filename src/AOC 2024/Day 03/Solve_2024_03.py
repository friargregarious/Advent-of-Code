"""
###############################################################################
#
#                              ADVENT OF CODE: {year}
#                                  {title}
#                      {url}
#
###############################################################################
#
# SOLVER:   friargregarious (greg.denyes@gmail.com)
# SOLVED:   {date_solved}
# HOME:     https://github.com/friargregarious
# SOURCE:   https://github.com/friargregarious/AOC-2023
#
# WRITTEN AND TESTED IN PYTHON VER {version}
#
###############################################################################
"""
###############################################################################
# imports, globals and helper functions/classes

import os, time, argparse, re, aocd, toml, pickle, markdownify
from tracemalloc import start
from pathlib import Path
from bs4 import BeautifulSoup


def data(input_text_path:Path=Path("input.txt")):

    text_source_list = input_text_path.read_text(encoding="UTF-8").split("\n")

    return text_source_list
 
def mul(a:str, b:str)->int:
     return int(a) * int(b)

###############################################################################
# PART A
###############################################################################
def solve_a(source):
    """for solving Part A"""

    # xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
    # pattern = re.Pattern()
    pattern=r'mul\(([0-9]{1,3}),([0-9]{1,3})\)'
    if _EXAMPLE:
        print(f"a --> pattern: {pattern}\nShould Find: mul(2,4) mul(5,5) mul(11,8) mul(8,5)")
    
    all_res = []
    total = 0

    for row in source:
        res = re.findall(pattern, row)
        all_res.append(res)

        if _EXAMPLE:
            print(f"a --> Row: {row}")
            print(f"a --> {res}")
        
        total += sum([mul(a,b) for a, b in res])

    return total


###############################################################################
# PART B
###############################################################################
def solve_b(source):
    """for solving Part B"""

    pattern = r"(do\(\)|don't\(\)|mul\(([0-9]{1,3}),([0-9]{1,3})\))"
    if _EXAMPLE:
        text = Path("example_b.txt").read_text(encoding="UTF-8")
    else:
        text = Path("input.txt").read_text(encoding="UTF-8")
    
    matches = re.findall(pattern, text)
    print("\n".join(map(str, matches)))
    mul_enabled = True
    solution = 0

    for match in matches:
        if match[0] == "do()":
            mul_enabled = True
        elif match[0] == "don't()":
            mul_enabled = False
        elif match[0].startswith("mul"):
            if mul_enabled:
                solution += int(match[1]) * int(match[2])

    print(f"B solution: {solution}")
    return solution


###############################################################################
def main(source, do_a=False, do_b=False):
    """ENTRY POINT FOR SUBMITTING & BENCHMARKING"""
    solution_a = solve_a(source=data(source)) if do_a else 0
    solution_b = solve_b(source=data(source)) if do_b else 0    

    return (solution_a, solution_b)


###############################################################################
# command line interface
if __name__ == "__main__":
    os.system('cls')
    config = toml.load(Path('.env'))
    _year = config['puzzle']['year']
    _day = config['puzzle']['day']
    _puzzle_path = config['puzzle']['path']
    _user = aocd.models.User(config['user']['token'])
    
    arg = argparse.ArgumentParser()
    arg.add_argument("--example", help="Test code with example input instead of default 'input.txt'.", type=bool, default=False)
    arg.add_argument("--parts", help="Chose parts 'A' or 'B' to run. (defaults to both: 'AB').", type=str, default="AB")
    arg.add_argument("--submit", help="Submit answer to server. (defaults to False).", type=bool, default=False)
    args = arg.parse_args()
    
    # save puzzle info
    
    if Path(config['puzzle']['path']).is_file():
        puzzle = pickle.load(open(_puzzle_path, "rb"))
        puzzle._user = _user
        print(f"Found existing puzzle file: {_puzzle_path}")
    else:
        puzzle = aocd.models.Puzzle(year=_year, day=_day, user=_user)
        pickle.dump(puzzle, open(_puzzle_path, "wb"))
        print(f"Creating new puzzle file: {_puzzle_path}")
    
    DOA = "A" in args.parts.upper()
    DOB = "B" in args.parts.upper()

    if args.example:
        print(f"** Args: {args}")
        source_input = Path("example_a.txt")
        _EXAMPLE = True
    else:
        _EXAMPLE = False
        source_input = Path("input.txt")

    part_a, part_b = main(source_input, do_a=True, do_b=True)
    
    if DOA and args.submit and puzzle.answered_a:
        soup = BeautifulSoup( puzzle._get_prose().encode("utf-8"), "html.parser" )
        articles = "\n".join( [str(x) for x in soup.find_all("article")] )
        md_articles = markdownify.markdownify( articles, heading_style="ATX" )
        Path("README.md").write_text( md_articles )

    if DOA and args.submit and not puzzle.answered_a:
        puzzle.answer_a = part_a # type: ignore
        pickle.dump(puzzle, open(_puzzle_path, "wb"))
            
    if DOB and args.submit and not puzzle.answered_b:
        time.sleep(5) if DOA else None
        puzzle.answer_b = part_b # type: ignore
        pickle.dump(puzzle, open(_puzzle_path, "wb"))
        
    if puzzle.answered_a:
        print(f"Part A is completed: {puzzle.answer_a}")
    else:
        print( "             Part A:", part_a)

    if puzzle.answered_b:
        print(f"Part B is completed: {puzzle.answer_b}")
    else:
        print( "             Part B:", part_b)
    