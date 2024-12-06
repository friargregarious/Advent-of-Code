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

import os, argparse, toml
from time import sleep
from markdownify import markdownify
from pathlib import Path
from . import solve_utilitites as su

def data(input_text_path:Path=Path("input.txt")):
    text_source_list = input_text_path.read_text(encoding="UTF-8").split("\n")
    return text_source_list


def whats_at(loc:tuple, word_search:list)->str:
    row, col = loc
    return word_search[row][col]

###############################################################################
# PART A
###############################################################################
def horizontal(starting_point:tuple, word_map:list):
    r, c = starting_point
    words = []

    max_c = len(word_map[r]) - 4
    min_c = 3

    dirs = {}
    
    # forwards
    if c <= max_c: dirs["forward"] = [ (r, c + x) for x in range(4) ]

    # backwards
    if c >= min_c: dirs["backward"] = [ (r, c - x) for x in range(4) ]
        
    # test & forward
    for d, locs in dirs.items():
        sample = "".join([ whats_at(loc, word_map) for loc in locs ])
        if sample == "XMAS":
            words.append(locs + [d])

    return words

def vertical(starting_point:tuple, word_map:list):
    r, c = starting_point
    words = []

    max_r = len(word_map) - 4
    min_r = 3

    dirs = {}

    # down
    if r <= max_r: dirs["down"] = [ (r+x, c) for x in range(4) ] 

    # up
    if r >= min_r: dirs["up"] = [ (r-x, c) for x in range(4) ]

    # test & forward
    for d, locs in dirs.items():
        sample = "".join([ whats_at(loc, word_map) for loc in locs ])
        if sample == "XMAS":
            words.append(locs + [d])


    return words

def diagonal(starting_point:tuple, word_map:list):
    r, c = starting_point
    words = []

    max_c = len(word_map[r]) - 4
    max_r = len(word_map) - 4
    min_c = 3
    min_r = 3

    directions = {}

    # up-right
    if r >= min_r and c <= max_c: directions["up-right"] =  [ (r-x, c+x) for x in range(4) ] 

    # down-right
    if r <= max_r and c <= max_c: directions["down-right"] = [ (r+x, c+x) for x in range(4) ] 

    # up-left
    if r >= min_r and c >= min_c: directions["up-left"] = [ (r-x, c-x) for x in range(4) ] 
        
    # down-left
    if r <= max_r and c >= min_c: directions["down-left"] = [ (r+x, c-x) for x in range(4) ] 
    
    for d, direction in directions.items():
        letters = [ whats_at(loc, word_map) for loc in direction ]
        sample = "".join(letters)
        # print("diagnals:", direction, sample)
        if sample == "XMAS":
            words.append( direction + [d])
    
    return words

def solve_a(word_search:list):
    """for solving Part A"""

    found = []
    for r, row in enumerate(word_search):
        for c, char in enumerate(row):
            if char == "X":
                found.extend(horizontal((r, c), word_search))
                found.extend(vertical((r, c), word_search))
                found.extend(diagonal((r, c), word_search))

    # for word in found:
    #     print(word)
    
    return len(found)


###############################################################################
# PART B
###############################################################################
def x_mas_search(loc:tuple, word_search:list):
    """
    Given a location in the word search, will return a dictionary with all the orientations that have the string "MAS" in them.
    The dictionary will have the location as the key and the value will be another dictionary with the orientation as the key and the list of locations as the value.
    For example, if the word search is:
       ..M..
       .MAS.
       ..S..
       .....
    And the location is (1, 2), the function will return 
    { (1, 2) : [ [(0, 2), (1, 2), (3, 2), "DOWN"], [(1, 3), (1, 2), (1, 1), "RIGHT"] ] }
    """
    
    r, c = loc
    # we assume we are in the middle, that (r, c) is an "A"
    
    min_r = 1
    min_c = 1
    max_r = len(word_search) - 2
    max_c = len(word_search[r]) - 2
    
    if min_r <= r <= max_r and min_c <= c <= max_c:
        bearing = {
            # "UP" : [(r+1, c), (r, c), (r-1, c)],
            # "DOWN" : [(r-1, c), (r, c), (r+1, c)],
            # "RIGHT" : [(r, c+1), (r, c), (r, c-1)],
            # "LEFT" : [(r, c-1), (r, c), (r, c+1)],
            "UP-LEFT" : [(r+1, c-1), (r, c), (r-1, c+1)],
            "UP-RIGHT" : [(r+1, c+1), (r, c), (r-1, c-1)],
            "DOWN-LEFT" : [(r-1, c-1), (r, c), (r+1, c+1)],
            "DOWN-RIGHT" : [(r-1, c+1), (r, c), (r+1, c-1)],
            }
        
        spokes = []
        for b, locs in bearing.items():
            if "MAS" == "".join([ whats_at(loc, word_search) for loc in locs ]):
                spokes.append(locs + [b] + ["MAS"])
    
        if len(spokes) >= 2:
            # f"({r}, {c})": spokes
            return { (r,c): spokes }

    return {}
    
    
def solve_b(source):
    """for solving Part B"""
    found = {}
    
    for r, row in enumerate(source):
        for c, char in enumerate(row):
            if char == "A":
                l = (r, c)
                found.update(x_mas_search(l, source))

    # Path("B_ANSWERS.toml").write_text(toml.dumps(found))
    return len(found)



###############################################################################
# command line interface
if __name__ == "__main__":
    os.system('cls')
    
    # Collect command line arguments
    arg = argparse.ArgumentParser()
    arg.add_argument("-e", "--example", help="Bool Flag: Test code with example input instead of default 'input.txt'.", default=False, action="store_true")
    arg.add_argument("-s", "--submit", help="Bool Flag: Submit answer to server. (defaults to False).", default=False, action="store_true")
    arg.add_argument("-b", "--part_b", help="Bool Flag: Choses parts 'A' or 'B' to run. (defaults to 'A').", default=False, action="store_true")
    arg.add_argument("-r", "--refresh", help="Bool Flag: Refresh/update the readme.md file and exit.", default=False, action="store_true")
    arg.add_argument("-d", "--discord", help="Bool Flag: Send message to discord channel and exit.", default=False, action="store_true")
    args = arg.parse_args()
    
    su.print_args(vars(args))

    # Load puzzle parameters
    config = toml.load(Path('.env'))
    _puzzle_path = config['puzzle']['path']
    
    DO_A = not args.part_b
    DO_B = args.part_b
    DO_EXAMPLE = args.example
    SUBMIT_PUZZLE = args.submit
    REFRESH = args.refresh
    DISCORD = args.discord
    
    # open puzzle info
    puzzle = su.open_puzzle(_puzzle_path)
    
    if REFRESH:
        su.refresh_readme(puzzle)

    # Setup input data
    if DO_EXAMPLE and DO_A:
        result = solve_a(data(Path("example_a.txt")))
    elif DO_EXAMPLE and DO_B:
        result = solve_b(data(Path("example_b.txt")))
    else:
        source_input = data(Path("input.txt"))
        if DO_A:
            result = solve_a(source_input)
        else:
            result = solve_b(source_input)

    if SUBMIT_PUZZLE:
        p = "A" if DO_A else "B"
        su.submit_result(puzzle, result, p, _puzzle_path)
