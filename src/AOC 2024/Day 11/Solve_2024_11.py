"""
################################################################################
#                                                                              #
#                             ADVENT OF CODE: 2024                             #
#                              Plutonian Pebbles                               #
#                     https://adventofcode.com/2024/day/11                     #
#                                                                              #
################################################################################
#                                                                              #
# A SOLVED:   2024-12-11 08:17                                                 #
# SOLVER:     friargregarious (greg.denyes@gmail.com)                          #
# HOME:       https://github.com/friargregarious                               #
#                                                                              #
#                   WRITTEN AND TESTED IN PYTHON VER 3.13.0                    #
#                                                                              #
################################################################################
"""
###############################################################################
# imports, globals and helper functions/classes



from genericpath import isdir
from hmac import new
import os, argparse, toml, sys, json
import solve_utilities as su
from pathlib import Path


def str_gen(this_blink):
    WORK = Path( "work" )
    previous_blink = this_blink - 1
    old_blink = previous_blink - 1

    # for old_blinks in list(range(1, previous_blink)) + [this_blink]:
    #     todelete = WORK.glob(f"BLINK {old_blinks:02}*.stones")
    #     count_delete = len(list(todelete))
    #     if count_delete > 0:
    #         for file in todelete:
    #             print(f"Deleting {file} old files from BLINK {old_blinks:2} previous BLINK {previous_blink:2}")
    #             try:
    #                 file.unlink()
    #             except:
    #                 os.remove(file)    
    
    for i in range(1, previous_blink):
        old_folder:Path = WORK / f"BLINK {old_blink:02}"
        if old_folder.exists():
            try:
                for stone in old_folder.glob("*.stones"):
                    os.remove(stone)

                os.rmdir(old_folder)
            except OSError:
                for stone in old_folder.glob("*.stones"):
                    stone.unlink()
                os.rmdir(old_folder)                
            except:
                for stone in old_folder.glob("*.stones"):
                    stone.unlink()
                old_folder.rmdir()
                
    WORK_PREVIOUS = WORK / f"BLINK {previous_blink:02}"

    if this_blink == 1:
        print(f"Reading original input BLINK {previous_blink:2}")
        source_text = Path("input.txt").read_text(encoding="UTF-8")

        if DO_EXAMPLE:
            source_text = Path("example.txt").read_text(encoding="UTF-8")

        for old_blinks in map(int, source_text.split(" ")):
            yield old_blinks

    else:
        print(f"Reading data files for BLINK {previous_blink:2}")
        # source_files = sorted(WORK_PREVIOUS.glob(f"BLINK {previous_blink:02}*.stones"), reverse=False)
        for source in sorted(WORK_PREVIOUS.glob(f"BLINK {previous_blink:02}*.stones"), reverse=False):
            print(f"Blinking from {source.as_posix()}")
            for old_blinks in json.loads(source.read_text(encoding="UTF-8")):
                yield old_blinks

        source_text = source.read_text(encoding="UTF-8")

def blinker( BLINKS ):
    MAX_INDEX = 500_000
    WORK = Path( "work" ) 
    
    for BLINK in range(50, 1 + BLINKS):
        WORK = Path( "work" ) / f"BLINK {BLINK:02}"
        
        print(f"Now producing BLINK: {BLINK:2}")
        stone_count = 0
        file_count = 0
        new_source = []

        for item in str_gen(BLINK):
            if item == 0:
                # RULE 1: If number 0, replaced by the number 1.
                new_source.append( 1 )
                stone_count += 1
            
            elif len(str(item)) % 2 == 0:
                # RULE 2: If number has an even number of digits, it is replaced by two stones. The left half of the 
                # digitsare engraved on the new left stone, and the right half of the digits are engraved on 
                # the new right stone.
                # 123005 --> 123, 5
                new_source.append( int(str(item)[:len(str(item))//2]) )
                new_source.append( int(str(item)[len(str(item))//2:]) )
                stone_count += 2

            else:
                # RULE 3: If none of the other rules apply, multiplied by 2024.
                new_source.append( item * 2024 )
                stone_count += 1
                
            if len(new_source) >= MAX_INDEX:
                file_count += 1
                save_list, new_source = new_source[:MAX_INDEX], new_source[MAX_INDEX:]

                WORK.mkdir(exist_ok=True)
                file_target = WORK / f"BLINK {BLINK:02}_{file_count:08}.stones"
                file_target.write_text( json.dumps(save_list) )


        file_count += 1
        detail_text = f"Completed BLINK: {BLINK} with {stone_count:,} Stones, into {file_count:,} Files."
        print(detail_text) if file_count % 100 == 0 else None

        
        Path( "details.txt" ).write_text( detail_text )
        file_target = WORK / f"BLINK {BLINK:02}_{file_count:08}.stones"
        file_target.write_text( json.dumps(new_source) )
        
    
    return len(new_source)

def count_stones(initial_stones, blinks):
    # Dictionary to store stone counts based on number of digits (and other characteristics)
    stone_counts = { 0 : {i: initial_stones.count(i) for i in initial_stones} } 
    
    for n in range( 1, blinks +1 ):
        stone_counts[n] = {}

        for k, count in stone_counts[n-1].items():
            
            if k == 0:
                if 1 in stone_counts[n]:
                    stone_counts[n][1] += count
                else:
                    stone_counts[n][1] = count

            elif len(stone_str:= str(k)) % 2 == 0:
                mid = len(stone_str) // 2
                left, right =  int(stone_str[ :mid ]), int(stone_str[ mid: ] )

                if left in stone_counts[n]:
                    stone_counts[n][left] += count
                else:
                    stone_counts[n][left] = count

                if right in stone_counts[n]:
                    stone_counts[n][right] += count
                else:
                    stone_counts[n][right] = count

            else:  # k == 1:
                new_num = k * 2024
                if new_num in stone_counts[n]:
                    stone_counts[n][new_num] += count
                else:
                    stone_counts[n][new_num] = count
                    
    max_blink = max(stone_counts.keys())
    
    grand_total = sum(stone_counts[max_blink].values())

    return grand_total


###############################################################################
# PART A
###############################################################################
def solve_a(source):
    """for solving Part A"""
    work_source = "working_source.txt"    
    raw = Path(source).read_text(encoding="UTF-8")
    Path(work_source).write_text(raw)

    BLINKS = 25
    return blinker( BLINKS )


###############################################################################
# PART B
###############################################################################
def solve_b():
    """for solving Part B"""

    # work_source = "working_source.txt"    
    # raw = Path(source).read_text(encoding="UTF-8")
    # Path(work_source).write_text(raw)

    source_text = list(map(int,Path("input.txt").read_text(encoding="UTF-8").split(" ")))
    
    BLINKS = 75
    

    return count_stones(source_text, BLINKS)

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
        source_input = "example.txt" if DO_EXAMPLE else "input.txt"
        result = solve_a(source_input) if DO_A else solve_b()

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
