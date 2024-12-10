"""
################################################################################
#                                                                              #
#                             ADVENT OF CODE: 2024                             #
#                               Guard Gallivant                                #
#                     https://adventofcode.com/2024/day/6                      #
#                                                                              #
################################################################################
#                                                                              #
# A SOLVED:   2024-12-06 08:14                                                 #
# B SOLVED:   N/A                                                              #
# SOLVER:     friargregarious (greg.denyes@gmail.com)                          #
# HOME:       https://github.com/friargregarious                               #
#                                                                              #
#                   WRITTEN AND TESTED IN PYTHON VER 3.13.0                    #
#                                                                              #
################################################################################
"""
###############################################################################
# imports, globals and helper functions/classes


from hmac import new
import json
import os, sys, argparse, toml
import time
from pathlib import Path
import solve_utilities as su

ROOM_LIMITS = {
}

OUTPUT = Path("standard_path.json")

def data(input_text_path:Path=Path("input.txt")):
    global ROOM_LIMITS 
    
    room_map = {}
    rows = input_text_path.read_text(encoding="UTF-8").split("\n")
    ROOM_LIMITS = {
        "r_min" : 0,
        "c_min" : 0, 
        "r_max" : len(rows), 
        "c_max" : len(rows[0]),
        }
        
    for r, row in enumerate(rows):
        for c, here in enumerate(row):
            
            if here == "#":
                room_map[(r, c)] = "#"

            elif DO_B and here == ".":
                room_map[(r, c)] = "."
            
            elif here in ["^", "v", "<", ">"]:
                room_map["G"] = (here, (r, c))

            
        # room_map.append(row.split())
 
    return room_map

###############################################################################
# PART A
###############################################################################
class Guard():
    def __init__(self, room_map:dict):

        f, self.pos = room_map["G"]
        # del room_map["G"]

        if   f == "^" : self.faces = "N"
        elif f == "v" : self.faces = "S"
        elif f == ">" : self.faces = "E"
        elif f == "<" : self.faces = "W"
    
    def move_forward(self):
        # print(f"Moving {self.faces} from {self.pos} to {self.next_step}") if DO_EXAMPLE else None
        self.pos = self.next_step
    
    @property
    def next_step(self):
        r, c = self.pos
        
        if self.faces == "N": return (r - 1, c)
        elif self.faces == "S": return (r + 1, c)
        elif self.faces == "E": return (r, c + 1)
        elif self.faces == "W": return (r, c - 1)

        raise ValueError
                
    def turn_right(self):
        dirs = ["N", "E", "S", "W"]
        turn_to = dirs[(dirs.index(self.faces) + 1) % 4]
        # print(f"Turning from {self.faces} to {turn_to}") if DO_EXAMPLE else None
        self.faces = turn_to
    

def is_item(room_position, room_map:dict):
    if room_position in room_map:
        return True
    return False


def is_in_room(grd:Guard):
    r, c = grd.pos

    tests = [
        ROOM_LIMITS["r_min"] <= r < ROOM_LIMITS["r_max"],
        ROOM_LIMITS["c_min"] <= c < ROOM_LIMITS["c_max"]
    ]
    return all(tests)


def string_loc(guard):
    return f"{guard.faces}-{guard.pos}"

        
def make_path(room_map):    
    guard = Guard(room_map)
    # visited = set()
    # visited.add(guard.pos)

    grd_path = []

    grd_path.append(string_loc(guard)) if DO_B else grd_path.append(guard.pos)

    looping = len( grd_path ) != len( set(grd_path) ) if DO_B else False
        
    while is_in_room( guard ) and not looping:
        if DO_B: looping = len( grd_path ) != len( set(grd_path) ) 
        
        s_loc = string_loc(guard)
        grd_path.append(s_loc if DO_B else guard.pos)

        if DO_B and looping:
            return True, grd_path
            
        if is_item(guard.next_step, room_map):
            guard.turn_right()

        guard.move_forward()




    return grd_path

def solve_a(room_map):
    """for solving Part A"""

    # !!!!! My FIRST EVER walrus expression !!!!!
    visited = set(grd_path := make_path(room_map))

    steps_taken = { str(grd_path.index(step)): step for step in grd_path }

    print(f"Visited: {visited}") if DO_EXAMPLE else None
    print(f"Guard path: {grd_path}") if DO_EXAMPLE else None
    OUTPUT.write_text(json.dumps(steps_taken, indent=3))
    return len(visited)


def draw(room_map):
    for r in range(ROOM_LIMITS["r_min"], ROOM_LIMITS["r_max"]):
        for c in range(ROOM_LIMITS["c_min"], ROOM_LIMITS["c_max"]):
            print(room_map[(r, c)], end="") if (r,c) in room_map else print(".", end="")
        print()

###############################################################################
# PART B
###############################################################################
def solve_b(room_map):
    """for solving Part B"""


    # empty_squares = [k for k, v in room_map.items() if v == "."]
    path_loops = []
    if OUTPUT.is_file():
        standard_path = json.loads(OUTPUT.read_text(encoding="UTF-8"))
    else:
        # print("No standard guard path file found.")
        raise FileNotFoundError(f"Standard guard path file {OUTPUT.as_posix()} not found.")
        # sys.exit(1)

    for _, location in standard_path.items():
        new_obstacle = tuple(location)
        print(f"Trying -> {new_obstacle}.")
        temp_map = room_map.copy()
        temp_map[new_obstacle] = "#"
        # guard = Guard(temp_map)

        looped, grd_path = make_path(temp_map)
        if looped:
            path_loops.append( grd_path )

        # visited.add(f"{guard.faces} {guard.pos}")
        print(f"Trying {new_obstacle}", path_loops[-1])

        
    return len(path_loops)


###############################################################################
# command line interface
###############################################################################
if __name__ == "__main__":
    os.system('cls')
    
    # Collect command line arguments
    arguments = argparse.ArgumentParser()
    arguments.add_argument("-e", "--example", help="Bool Flag: Test code with example input instead of default 'input.txt'.", default=False, action="store_true")
    arguments.add_argument("-s", "--submit", help="Bool Flag: Submit answer to server. (defaults to False).", default=False, action="store_true")
    arguments.add_argument("-b", "--part_b", help="Bool Flag: Choses parts 'A' or 'B' to run. (defaults to 'A').", default=False, action="store_true")
    arguments.add_argument("-r", "--refresh", help="Bool Flag: Refresh/update the readme.md file and exit.", default=False, action="store_true")
    arguments.add_argument("-d", "--discord", help="Bool Flag: Send message to discord channel and exit.", default=False, action="store_true")
    arguments.add_argument("-v", "--verbose", help="Bool Flag: allow in code print statements.", default=False, action="store_true")
    
    args = arguments.parse_args()

    su.print_args(vars(args))

    # Load puzzle parameters
    config = toml.load(Path('.env'))
    
    DO_A, DO_B = not args.part_b, args.part_b
    DO_EXAMPLE = args.example
    VERBOSE = args.verbose
    
    # open puzzle info
    puzzle = su.open_puzzle(config)

    if args.discord:
        su.Discord(puzzle=puzzle, config=config)
        sys.exit()
    
    if args.refresh:
        su.refresh_readme(puzzle)
        sys.exit()

    if args.submit:
        p = "A" if DO_A else "B"

        f_ex = '(From Example)' if DO_EXAMPLE else '(From input)'
        source_input = data( Path("example_a.txt") ) if DO_EXAMPLE else data( Path("input.txt") )
        result = solve_a(source_input) if DO_A else solve_b(source_input)

        correct_msg = ""
        match f"{'EXPL' if DO_EXAMPLE else 'REAL'}, {p}":
            case "EXPL, A": correct_answer = puzzle.examples[0].answer_a
            case "EXPL, B": correct_answer = puzzle.examples[0].answer_b
            # case "EXPL, B": correct_answer = '34' # puzzle file is corrupt.
            case "REAL, A": correct_answer = puzzle.answer_a if puzzle.answered_a else "unknown"
            case "REAL, B": correct_answer = puzzle.answer_b if puzzle.answered_b else "unknown"
            case _: correct_answer = "unknown"
        
        compare = correct_answer == str(result)
        correct_msg = f"IS CORRECT!! ({correct_answer})" if compare else f"IS NOT CORRECT ({correct_answer})"

        print( f"Solution ({p}): {result} {correct_msg} {f_ex}" )
        if not DO_EXAMPLE: su.submit_result(puzzle, result, p, config)
