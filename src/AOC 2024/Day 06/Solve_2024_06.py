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


import os, argparse, toml
from markdownify import markdownify
from pathlib import Path
import solve_utilities as su

ROOM_LIMITS = {
}


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
                
            if here in ["^", "v", "<", ">"]:
                room_map[("G")] = (here, (r, c))
            
        # room_map.append(row.split())
 
    return room_map

###############################################################################
# PART A
###############################################################################
class Guard():
    def __init__(self, room_map:dict):
        f, self.pos = room_map["G"]

        if   f == "^" : self.faces = "N"
        elif f == "v" : self.faces = "S"
        elif f == ">" : self.faces = "E"
        elif f == "<" : self.faces = "W"
    
    def move_forward(self, room_map):
        print(f"Moving {self.faces} from {self.pos} to {self.next_step}") if DO_EXAMPLE else None
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
        print(f"Turning from {self.faces} to {turn_to}") if DO_EXAMPLE else None
        self.faces = turn_to
    

def is_item(room_position, room_map:dict):
    if room_position in room_map:
        return True
    return False


def is_in_room(grd:Guard, room_map:dict):
    r, c = grd.pos

    tests = [
        ROOM_LIMITS["r_min"] <= r < ROOM_LIMITS["r_max"],
        ROOM_LIMITS["c_min"] <= c < ROOM_LIMITS["c_max"]
    ]
    return all(tests)
        
        
def solve_a(room_map):
    """for solving Part A"""
    guard = Guard(room_map)
    visited = set()
    grd_path = []
    visited.add(guard.pos)
    grd_path.append(guard.pos)
    
    while is_in_room(guard, room_map):
        visited.add(guard.pos)
        grd_path.append(guard.pos)

        if is_item(guard.next_step, room_map):            
            guard.turn_right()

        guard.move_forward(room_map)


    print(f"Visited: {visited}") if DO_EXAMPLE else None
    print(f"Guard path: {grd_path}") if DO_EXAMPLE else None
    return len(visited)

###############################################################################
# PART B
###############################################################################
def solve_b(source):
    """for solving Part B"""

    return 0


###############################################################################
# command line interface
###############################################################################
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
    puzzle = su.open_puzzle(config)
    
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

    print(f"Answer Part {'A' if DO_A else 'B'}: {result}  {'(Example)' if DO_EXAMPLE else ''}")
    
    if SUBMIT_PUZZLE:
        p = "A" if DO_A else "B"
        su.submit_result(puzzle, result, p, _puzzle_path)

