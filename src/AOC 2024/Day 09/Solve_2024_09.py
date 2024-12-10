"""
################################################################################
#                                                                              #
#                             ADVENT OF CODE: 2024                             #
#                               Disk Fragmenter                                #
#                     https://adventofcode.com/2024/day/9                      #
#                                                                              #
################################################################################
#                                                                              #
# A SOLVED:   2024-12-09 18:59                                                 #
# SOLVER:     friargregarious (greg.denyes@gmail.com)                          #
# HOME:       https://github.com/friargregarious                               #
#                                                                              #
#                   WRITTEN AND TESTED IN PYTHON VER 3.13.0                    #
#                                                                              #
################################################################################
"""
###############################################################################
# imports, globals and helper functions/classes

import os, argparse, toml, sys, json
import solve_utilities as su
from pathlib import Path
from math import prod


def data(input_text_path:Path=Path("input.txt")):
    text_source_list = input_text_path.read_text(encoding="UTF-8")

    if not DO_EXAMPLE and len(text_source_list) != 19_999:
        print(len(text_source_list), "does not match 19,999 characters!!!")

    return text_source_list

###############################################################################
# PART A
###############################################################################

def step_0(DISKMAP):
    # STEP 0: BUILD DATA
    print( "-" * 60 )
    print("STEP 0: BUILD DATA ".ljust(60, "-"))
    file_parts = [ int(x) for x in DISKMAP[::2] ] 
    spaces = [ int(x) for x in str(DISKMAP[1::2] + "0") ] 
    if DO_EXAMPLE:
        print( "DISKMAP:", DISKMAP )
        print( "file_parts:", file_parts )
        print( "    spaces: ", spaces )
        print( "-" * 60 )

    return file_parts, spaces

def step_1(file_parts, spaces):
    # STEP 1: BUILD FILE BLOCKS FROM DISK MAP
    print("STEP 1: BUILD FILE BLOCKS FROM DISK MAP ".ljust(60, "-"))
    FILEBLOCKS = []
    for i, file_part in enumerate( file_parts ):
        # FILEBLOCKS.append( str(i) * file_part )
        FILEBLOCKS.extend( [str(i) for _ in range(file_part)] )
        
        # FILEBLOCKS.append( "." * spaces[i] )
        FILEBLOCKS.extend( [str(".") for _ in range(spaces[i])] )
        
    if DO_EXAMPLE:
        print( FILEBLOCKS )
        fb = "".join(FILEBLOCKS)
        EXAMPLE = "00...111...2...333.44.5555.6666.777.888899"
        print( "FILEBLOCKS:", fb )
        print( "   EXAMPLE:", EXAMPLE )
        print( "FILEBLOCKS == EXAMPLE: ", "".join(FILEBLOCKS) == EXAMPLE )
        print( "-" * 60 )

    return FILEBLOCKS

def step_2(FILEBLOCKS):
    # STEP 2: MOVE FILE BLOCKS LEFT
    print("STEP 2: MOVE FILE BLOCKS LEFT ".ljust(60, "-"))

    FRAGEDBLOCKS = FILEBLOCKS.copy()
    while True:
        if "." not in FRAGEDBLOCKS:
            FRAGEDBLOCKS = list(map(int, FRAGEDBLOCKS))
            break

        else:
            replace_this = FRAGEDBLOCKS.index(".")
            replace_with = FRAGEDBLOCKS.pop()
            while replace_with == ".":
                replace_with = FRAGEDBLOCKS.pop()
                
            FRAGEDBLOCKS[replace_this] = replace_with


    if DO_EXAMPLE:
        # print(FRAGEDBLOCKS)
        FRAGEDBLOCKS_str = "".join(map(str,FRAGEDBLOCKS))
        EXAMPLE = "0099811188827773336446555566"
        print("FRAGEDBLOCKS:", FRAGEDBLOCKS_str)
        print("     EXAMPLE:", EXAMPLE )
        print( "FRAGEDBLOCKS == EXAMPLE:",  FRAGEDBLOCKS_str == EXAMPLE )
        
    return FRAGEDBLOCKS



def step_3(FRAGEDBLOCKS:list):
    # STEP 3: FILESYSTEM CHECKSUM
    print( "-" * 60 )
    print("STEP 3: FILESYSTEM CHECKSUM ".ljust(60, "-"))
    if not DO_EXAMPLE:
        print(f"Received from step_2{'a' if DO_A else 'b'}():")
        print( "...", FRAGEDBLOCKS[25:50], "...")

    checksum = 0
    for i, x in enumerate(FRAGEDBLOCKS):
        if "." not in x: checksum += prod( [i, int(x)] )
    
    return checksum



def solve_a(DISKMAP):
    """for solving Part A"""

    file_parts, spaces = step_0(DISKMAP)
    FILEBLOCKS = step_1(file_parts, spaces)
    FRAGEDBLOCKS = step_2(FILEBLOCKS)
    return step_3(FRAGEDBLOCKS)



###############################################################################
# PART B
###############################################################################

def step_1_b(file_parts, spaces):
    # STEP 1: BUILD FILE BLOCKS FROM DISK MAP
    print("STEP 1b: BUILD FILE BLOCKS FROM DISK MAP ".ljust(60, "-"))
    FILEBLOCKS = []
    for i, file_part in enumerate( file_parts ):
        # FILEBLOCKS.append( str(i) * file_part )
        FILEBLOCKS.extend( [str(i) for _ in range(file_part)] )
        
        # FILEBLOCKS.extend( [str(".") for _ in range(spaces[i])] )
        FILEBLOCKS.append( "." * spaces[i] )

    FILEBLOCKS.remove('')
    if DO_EXAMPLE:
        print( FILEBLOCKS )
        fb = "".join( FILEBLOCKS )
        EXAMPLE = "00...111...2...333.44.5555.6666.777.888899"
        print( "FILEBLOCKS:", fb )
        print( "   EXAMPLE:", EXAMPLE )
        print( "FILEBLOCKS == EXAMPLE: ", "".join(FILEBLOCKS) == EXAMPLE )
        print( "-" * 60 )

    return FILEBLOCKS


def step_2_b(FRAGEDBLOCKS:list):
    # STEP 2: MOVE FILE BLOCKS LEFT
    print("STEP 2b: MOVE FILE BLOCKS LEFT ".ljust(60, "-"))
    
    if DO_EXAMPLE:
        print("FRAGEDBLOCKS:".rjust(20), FRAGEDBLOCKS)
        print("FRAGEDBLOCKS:".rjust(20), "".join(FRAGEDBLOCKS), "\n")
    # else:
    #     print("FRAGEDBLOCKS:".rjust(20), FRAGEDBLOCKS[:50])
    #     print("FRAGEDBLOCKS:".rjust(20), "".join(FRAGEDBLOCKS[:50]), "\n")

    this_file_name:int = 0 # max([int(a) for a in FRAGEDBLOCKS if a.isdecimal() ])
    for i in FRAGEDBLOCKS:
        if str(i).isdecimal() and this_file_name < int(i): this_file_name = int(i)


    while this_file_name >= 0:
        file_size:int = FRAGEDBLOCKS.count(str(this_file_name))
        this_file_index:int = FRAGEDBLOCKS.index(str(this_file_name))
        # print(f"Idx: {this_file_name:2} size: {file_size:2}:".rjust(20), "".join(FRAGEDBLOCKS)[:50] )
        
        
        for i, blank in enumerate(FRAGEDBLOCKS[:this_file_index]):
            if isinstance(blank, str) and "." in blank and len(blank) >= file_size:

                # get rid of the old file
                oldf = str(this_file_name)
                while oldf in FRAGEDBLOCKS:
                    FRAGEDBLOCKS[FRAGEDBLOCKS.index(oldf)] = '.'

                # put the file into the next blank space that fits
                blank_length = len(blank)
                FRAGEDBLOCKS.pop(i)
                leftovers = ''
                for n in range(blank_length):
                    if n < file_size: 
                        FRAGEDBLOCKS.insert(i+n, str( this_file_name ) )
                    else:
                        leftovers += '.'
                if leftovers != '': FRAGEDBLOCKS.insert(i + file_size, leftovers )

                break
        
        this_file_name -= 1

    
    new_FRAGGED = []
    for x in FRAGEDBLOCKS:
        if isinstance(x, str) and '.' in x:
            for i in range(len(x)):
                new_FRAGGED.append(".")
        elif x.isdecimal():
            new_FRAGGED.append(str(x))
 

    if DO_EXAMPLE:
        # print(FRAGEDBLOCKS)
        fraged = "".join(new_FRAGGED)
        print(f"FRAGEDBLOCKS:".rjust(14), fraged )

        if DO_A:
            EXAMPLE = "0099811188827773336446555566.............."
        else:
            EXAMPLE = "00992111777.44.333....5555.6666.....8888.."

        print(f" {'A' if DO_A else 'B'} EXAMPLE:".rjust(14), EXAMPLE)
        print( "FRAGEDBLOCKS == EXAMPLE:",  fraged == EXAMPLE )

        mistakes = "".join([ ' ' if a==b else '^' for a, b in zip(EXAMPLE, "".join(new_FRAGGED)) ])
        if "^" in mistakes: print( 'MISTAKES'.rjust(14), mistakes )
    
    Path("defraged_2b.json").write_text(json.dumps({i: x for i, x in enumerate(FRAGEDBLOCKS)}))       
    Path("defrag_clean_2b.json").write_text(json.dumps({i: x for i, x in enumerate(new_FRAGGED)}))

    
    
    return new_FRAGGED


def solve_b(DISKMAP):
    """for solving Part B"""

    file_parts, spaces = step_0(DISKMAP) # no change
    
    FILEBLOCKS = step_1_b(file_parts, spaces)
    # FILEBLOCKS = [ 0, 0, "...", 1, 1, 1, "...", 2, "...", 3, 3, 3, ".", 4, 4, 
    #               ".", 5, 5, 5, 5, ".", 6, 6, 6, 6, ".", 7, 7, 7, ".", 8, 8, 
    #               8, 8, 9, 9 ]
        
    FRAGEDBLOCKS = step_2_b(FILEBLOCKS)


    return step_3(FRAGEDBLOCKS)


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

    if args.refresh:
        su.refresh_readme(puzzle)
        sys.exit()

    if args.discord:
        su.Discord(puzzle=puzzle, config=config)
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
        if not DO_EXAMPLE: 
            su.submit_result(puzzle, result, p, config)
            if puzzle.answered_a and not puzzle.answered_b: su.refresh_readme(puzzle)
            if puzzle.answered_b: su.Discord(puzzle=puzzle, config=config)


