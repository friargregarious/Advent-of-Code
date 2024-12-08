"""
################################################################################
#                                                                              #
#                             ADVENT OF CODE: 2024                             #
#                            Resonant Collinearity                             #
#                     https://adventofcode.com/2024/day/8                      #
#                                                                              #
################################################################################
#                                                                              #
# A SOLVED:   2024-12-08 02:07                                                 #
# SOLVER:     friargregarious (greg.denyes@gmail.com)                          #
# HOME:       https://github.com/friargregarious                               #
#                                                                              #
#                   WRITTEN AND TESTED IN PYTHON VER 3.13.0                    #
#                                                                              #
################################################################################
"""
###############################################################################
# imports, globals and helper functions/classes

from calendar import c
import json
import os, argparse, toml, sys
import solve_utilities as su
from string import ascii_letters, digits
from pathlib import Path

FREQS = ascii_letters + digits
LIMITS = {"r_min" : 0, "c_min" : 0, "r_max" : 0, "c_max" : 0}

class Loc:
    def __init__(self, f:str, row:int, col:int, ntype: str = "#") -> None:
        self.freq = f
        self.r = row
        self.c = col
        self.type = ntype

    def __repr__(self) -> str:
        # return f"{self.freq}({self.r:02}, {self.c:02})"
        return f"({self.r:02}, {self.c:02})"
    
    def __hash__(self) -> int:
        return hash(self.__repr__())
        
    def __add__(self, other:tuple):
        return Loc(self.freq, self.r + other[0], self.c + other[1])
    
    def __sub__(self, other:tuple):
        return Loc(self.freq, self.r - other[0], self.c - other[1])
    
    def __eq__(self, other)->bool:
        if isinstance(other, Loc):
            tests = [
                self.r == other.r,
                self.c == other.c
            ]
        elif isinstance(other, tuple):
            tests = [
                self.r == other[0],
                self.c == other[1]
            ]
        else:
            print(f"Unsupported type: {type(other)}")
            raise TypeError(f"Unsupported type: {type(other)}")

        return all(tests)
    
    def __ne__(self, other)->bool:
        return not self.__eq__(other)
    
    def __lt__(self, other):
        return (self.r, self.c) < (other.r, other.c)
    
    def __gt__(self, other):
        return (self.r, self.c) > (other.r, other.c)


def difference(a, b):
    row = abs(a.r - b.r)
    col = abs(a.c - b.c)
    return (row, col)

def is_on_grid(loc):
    tests = [
        LIMITS["r_min"] <= loc.r < LIMITS["r_max"],
        LIMITS["c_min"] <= loc.c < LIMITS["c_max"]
    ]
    return all(tests)


def draw_map( nodes, part ):
    file = Path(f"map_{part}.txt")
    with file.open("w") as f:
        for r in range(LIMITS["r_min"], LIMITS["r_max"]):
            for c in range(LIMITS["c_min"], LIMITS["c_max"]):
                point = "."
                for node in nodes:
                    if node == (r, c): point = "#"
                print(point, end="", file=f)
            print( file=f )



def data(input_text_path:Path=Path("input.txt")):
    """for reading puzzle data"""
    global LIMITS    
    LIMITS = {
        "r_min" : 0,
        "c_min" : 0, 
        "r_max" : len(input_text_path.read_text(encoding="UTF-8").split("\n")), 
        "c_max" : len(input_text_path.read_text(encoding="UTF-8").split("\n")[0]),
    }
    
    towers = {}

    for r, row in enumerate(input_text_path.read_text(encoding="UTF-8").split("\n")):
        for c, item in enumerate(row):
            if item in FREQS:
                if item in towers:
                    towers[item].append( Loc(item, r, c) )
                else:
                    towers[item] = [ Loc(item, r, c) ]

    sorted_towers = [f"{k}, {sorted(v)}" for k, v in sorted(towers.items(), key=lambda item: item[0])]
    Path("towers.txt").write_text( "\n".join(sorted_towers) )
    return towers


###############################################################################
# PART A
###############################################################################
def solve_a(TWRS):
    """for solving Part A"""
    antinodes = set()

    for freq, towers in TWRS.items():
        # print(f"{freq}: {towers}")
        # if freq not in antinodes: antinodes[freq] = []
        others = towers.copy()
        for i in towers:
            for o in others:
                if i != o:
                    diff = difference(i, o)
                    new_row = o.r - diff[0] if o.r < i.r else o.r + diff[0]
                    new_col = o.c - diff[1] if o.c < i.c else o.c + diff[1]
                    new_Loc = Loc(freq, new_row, new_col)
                    if is_on_grid(new_Loc): antinodes.add( new_Loc )
    
    # for node in antinodes:
    #     print(node)

    draw_map(antinodes, "a")

    text = "\n".join([str(x) for x in antinodes])
    Path("antinodes_a.text").write_text( text )
    return len(antinodes)
        

###############################################################################
# PART B
###############################################################################
def solve_b(TWRS):
    """for solving Part B"""
    antinodes = set()
    node_count = 0
    for freq, towers in TWRS.items():
        # print(f"{freq}: {towers}")
        # if freq not in antinodes: antinodes[freq] = []
        if len(towers) < 2: continue
        
        others = towers.copy()
        for i in towers:
            # antinodes.add( i )
            
            for o in others:
                if i != o:
                    diff = difference(i, o)
                    antinodes.add( o )
                    new_row = o.r - diff[0] if o.r < i.r else o.r + diff[0]
                    new_col = o.c - diff[1] if o.c < i.c else o.c + diff[1]
                    new_Loc = Loc(i.freq, new_row, new_col)
                    while is_on_grid(new_Loc):
                        antinodes.add( new_Loc )
                        
                        node_count += 1
                        # print("Antinodes:",antinodes)
                        new_row = new_Loc.r - diff[0] if new_Loc.r < i.r else new_Loc.r + diff[0]
                        new_col = new_Loc.c - diff[1] if new_Loc.c < i.c else new_Loc.c + diff[1]
                        new_Loc = Loc(i.freq, new_row, new_col)
    
    # for node in antinodes:
    #     print(node)

    draw_map(antinodes, "b")
    text = "\n".join([str(x) for x in antinodes])
    Path("antinodes_b.text").write_text( text )
    
    print(f"Node count: {node_count}")
    return len(antinodes)


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
            # case "EXPL, B": correct_answer = puzzle.examples[0].answer_b
            case "EXPL, B": correct_answer = '34' # puzzle file is corrupt.
            case "REAL, A": correct_answer = puzzle.answer_a if puzzle.answered_a else "unknown"
            case "REAL, B": correct_answer = puzzle.answer_b if puzzle.answered_b else "unknown"
            case _: correct_answer = "unknown"
        
        compare = correct_answer == str(result)
        correct_msg = f"IS CORRECT!! ({correct_answer})" if compare else f"IS NOT CORRECT ({correct_answer})"

        print( f"Solution ({p}): {result} {correct_msg} {f_ex}" )
        if not DO_EXAMPLE: su.submit_result(puzzle, result, p, config)
