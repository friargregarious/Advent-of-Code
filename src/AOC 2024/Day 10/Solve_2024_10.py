"""
################################################################################
#                                                                              #
#                             ADVENT OF CODE: 2024                             #
#                                   Hoof It                                    #
#                     https://adventofcode.com/2024/day/10                     #
#                                                                              #
################################################################################
#                                                                              #
# A SOLVED:   2024-12-10 19:31                                                 #
# SOLVER:     friargregarious (greg.denyes@gmail.com)                          #
# HOME:       https://github.com/friargregarious                               #
#                                                                              #
#                   WRITTEN AND TESTED IN PYTHON VER 3.13.0                    #
#                                                                              #
################################################################################
"""

###############################################################################
# imports, globals and helper functions/classes

import os, argparse, sys
import aocd, solve_utilities as su
from pathlib import Path

DO_A:bool = True 
DO_B:bool = not DO_A 
DO_EXAMPLE = False
VERBOSE = False
DISCORD = False

MAX_ROW = 0
MAX_COL = 0

def data(input_text_path: Path = Path("input.txt")):
    global MAX_ROW, MAX_COL, EXAMPLE
    MAX_ROW = len(input_text_path.read_text(encoding="UTF-8").split("\n"))
    MAX_COL = len(input_text_path.read_text(encoding="UTF-8").split("\n")[0])

    if DO_A:
        EXAMPLE = { (0, 2): 5, (0, 4): 6, (2, 4): 5,
                    (4, 6): 3, (5, 2): 1, (5, 5): 3,
                    (6, 0): 5, (6, 6): 3, (7, 1): 5, }

    if DO_B:
        # The sum of all trailhead ratings in this larger example topographic map is 81.
        EXAMPLE = { (0, 2): 20, (0, 4): 24, (2, 4): 10,
                    (4, 6): 4, (5, 2): 1, (5, 5): 4,
                    (6, 0): 5, (6, 6): 8, (7, 1): 5, }
        
        
        
        
    hiking_guide = {}
    trail_starts = []
    trail_ends = []

    for r, row in enumerate(input_text_path.read_text(encoding="UTF-8").split("\n")):
        for c, elevation in enumerate(row):
            height = int(elevation)
            loc = ( r, c )
            hiking_guide[loc] = height
            if height == 0:
                trail_starts.append(loc)
            if height == 9:
                trail_ends.append(loc)

    stuff = {
        "hiking_guide": hiking_guide,
        "trail_starts": trail_starts,
        "trail_ends": trail_ends,
    }

    msg =[
        (" hiking_guide:", len(hiking_guide)),
        (f" {len(trail_starts)} trail_starts:", trail_starts),
        (f" {len(trail_ends)} trail_ends:", trail_ends),
            ]
    
    for a, b in msg:
        print(a.replace("_", " ").title().rjust(20, "."), b)
    return stuff


def score_route(finds: dict):
    global EXAMPLE

    display = [ ("START POINT","EXPECTED","FOUND") ]
    display.extend( [ ( f"{key}", f"{val}", f"{len(set(finds[key]))}" if key in finds else "0" ) for key, val in EXAMPLE.items()] )

    if DO_EXAMPLE:
        print("-"*60)
        print(" Scores:",  list(sorted(map(str, finds.keys()))))
        print("EXAMPLE:",  list(sorted(map(str, EXAMPLE.keys()))))
        print("-"*60)

        for a, b, c in display:
            print(a.ljust(15), b.center(10), c.rjust(12))

    total = sum([len(set(x)) for x in finds.values()])

    return total


###############################################################################
# PART A
###############################################################################

def around_me(my_pos: tuple, topo: dict):
    global MAX_ROW, MAX_COL

    r, c = my_pos
    height = topo[my_pos]
    valid_dirs = []

    print(f"{r-1} >= 0 = {r-1>=0}") if VERBOSE else None
    if r - 1 >= 0 and height + 1 == topo[(r - 1, c)]:
        valid_dirs.append((r - 1, c))  # N
        
    print(f"{c-1} >= 0 = {c-1>=0}") if VERBOSE else None
    if c - 1 >= 0 and height + 1 == topo[(r, c - 1)]:
        valid_dirs.append((r, c - 1))  # W

    print(f"{r+1} < {MAX_ROW} = {r+1>MAX_ROW}") if VERBOSE else None
    if r + 1 < MAX_ROW and height + 1 == topo[(r + 1, c)]:
        valid_dirs.append((r + 1, c))  # S


    print(f"{c+1} < {MAX_COL} = {c+1>MAX_COL}") if VERBOSE else None
    if c + 1 < MAX_COL and height + 1 == topo[(r, c + 1)]:
        valid_dirs.append((r, c + 1))  # E

    print(f"Valid Dirs:", valid_dirs) if VERBOSE else None
    return valid_dirs


def solve_a(source: dict):
    """for solving Part A"""
    #     "hiking_guide" = {hiking_guide}  dict
    #     "trail_starts" = [trail_starts]  list

    topo = source["hiking_guide"]
    # STEP 1: STARTING POINTS
    routes: list = [{0: s} for s in source["trail_starts"]]
    finds = {s:[] for s in source["trail_starts"]}

    print(f"Routes:", routes) if VERBOSE else None
    current_step: int = 1
    while current_step < 10:
        print(f"Step: {current_step:3}\nRoutes Remaining: {len(routes)}") if VERBOSE else None
        
        done_trails: list = []

        while len(routes) > 0:
            this_trail: dict = routes.pop()
            print(f"\tThis Trail:", this_trail) if VERBOSE else None

            # EXAMPLE TRAIL
            # {0:(0,1), 1:(0,2), 2:(0,3), 3:(0,4), 4:(0,5), 5:(0,6), 6:(0,7), 7:(1,7), 8:(2,7), 9:(3,7)}

            if current_step not in this_trail:
                for step in around_me(this_trail[current_step - 1], topo):
                    this_trail[current_step] = step
                    print(f"\t\tTrail Continues: {this_trail}") if VERBOSE else None
                    done_trails.append(this_trail.copy())
            else:
                print(f"-> \t\tTrail Ends: {this_trail}") if VERBOSE else None
                done_trails.append(this_trail.copy())

        routes.extend(done_trails)
        print(f"Total Trails: {len(routes)}") if VERBOSE else None
        current_step += 1

    for r in routes:
        if r[0] in finds:
            finds[r[0]].append(f"{r[0]}->{r[9]}")
            print(r[0], finds[r[0]])
        else:
            print("MISSED ONE!")

    for r, v in finds.items():
        print(r)
        for l in v:
            print("\t\t", l)
            
    
    
    # finds = { finds[k] : len(list(v)) for k, v in finds.items() }
    
    return score_route(finds)


###############################################################################
# PART B
###############################################################################
def solve_b(source):
    """for solving Part B"""
    # Considering its trailheads in reading order, they have ratings of 
    # 20, 24, 10, 4, 1, 4, 5, 8, and 5. 
    # The sum of all trailhead ratings in this larger example topographic map is 81.

    print("Part B") if VERBOSE else None

    #     "hiking_guide" = {hiking_guide}  dict
    #     "trail_starts" = [trail_starts]  list

    topo = source["hiking_guide"]
    # STEP 1: STARTING POINTS
    routes: list = [{0: s} for s in source["trail_starts"]]
    finds = {s:[] for s in source["trail_starts"]}

    print(f"Routes:", routes) if VERBOSE else None
    current_step: int = 1
    while current_step < 10:
        print(f"Step: {current_step:3}\nRoutes Remaining: {len(routes)}") if VERBOSE else None
        
        done_trails: list = []

        while len(routes) > 0:
            this_trail: dict = routes.pop()
            print(f"\tThis Trail:", this_trail) if VERBOSE else None

            # EXAMPLE TRAIL
            # {0:(0,1), 1:(0,2), 2:(0,3), 3:(0,4), 4:(0,5), 5:(0,6), 6:(0,7), 7:(1,7), 8:(2,7), 9:(3,7)}

            if current_step not in this_trail:
                for step in around_me(this_trail[current_step - 1], topo):
                    this_trail[current_step] = step
                    print(f"\t\tTrail Continues: {this_trail}") if VERBOSE else None
                    done_trails.append(this_trail.copy())
            else:
                print(f"-> \t\tTrail Ends: {this_trail}") if VERBOSE else None
                done_trails.append(this_trail.copy())

        routes.extend(done_trails)
        print(f"Total Trails: {len(routes)}") if VERBOSE else None
        current_step += 1

    for r in routes:
        if r[0] in finds:
            finds[r[0]].append( "".join([f"{r[i]}" for i in r]) )
            print(r[0], finds[r[0]]) if VERBOSE else None
        else:
            print("MISSED ONE!") if VERBOSE else None

    for r, v in finds.items():
        print(r)
        for l in v:
            print("\t\t", l)


    return score_route(finds)


###############################################################################
# command line interface
###############################################################################
def main():
    global DO_A, DO_B, DO_EXAMPLE, VERBOSE, CONFIG

    if args.discord:
        su.Discord(puzzle=PUZZLE, config=CONFIG)
        sys.exit()

    if args.refresh:
        su.refresh_readme(PUZZLE)
        sys.exit()

    if args.submit:
        p = "A" if DO_A else "B"

        f_ex = "(From Example)" if DO_EXAMPLE else "(From input)"
        source_input = (
            data(Path("example_a.txt")) if DO_EXAMPLE else data(Path("input.txt"))
        )
        result = solve_a(source_input) if DO_A else solve_b(source_input)

        correct_msg = ""
        match f"{'EXPL' if DO_EXAMPLE else 'REAL'}, {p}":
            case "EXPL, A":
                correct_answer = PUZZLE.examples[0].answer_a
            case "EXPL, B": correct_answer = PUZZLE.examples[0].answer_b
            # case "EXPL, B": correct_answer = "34"  # puzzle file is corrupt.
            case "REAL, A":
                correct_answer = PUZZLE.answer_a if PUZZLE.answered_a else "unknown"
            case "REAL, B":
                correct_answer = PUZZLE.answer_b if PUZZLE.answered_b else "unknown"
            case _:
                correct_answer = "unknown"

        compare = correct_answer == str(result)
        correct_msg = (
            f"IS CORRECT!! ({correct_answer})"
            if compare
            else f"IS NOT CORRECT ({correct_answer})"
        )

        print(f"Solution ({p}): {result} {correct_msg} {f_ex}")
        if not DO_EXAMPLE:
            su.submit_result(PUZZLE, result, p, CONFIG)


if __name__ == "__main__":
    os.system("cls")
    # Collect command line arguments
    args:argparse.Namespace = su.gather_args().parse_args()
    su.print_args(vars(args))
    # global DO_A, DO_B, DO_EXAMPLE, VERBOSE, USER, PUZZLE, CONFIG, DISCORD
    
    # Load puzzle parameters and objects
    CONFIG:dict = su.get_config()  # toml.load(Path(".env"))
    USER:aocd.models.User = su.get_user(CONFIG)
    PUZZLE:aocd.models.Puzzle = su.open_puzzle(CONFIG)

    DO_B:bool = args.part_b
    DO_A:bool = not DO_B
    
    VERBOSE:bool = args.verbose
    DISCORD:bool = args.discord
    DO_EXAMPLE:bool = args.example
    
    main()
