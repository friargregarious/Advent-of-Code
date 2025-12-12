"""
################################################################################
#                                                                              #
#                          ADVENT OF CODE: 2025 DAY 5                          #
#                                  Cafeteria                                   #
#                     https://adventofcode.com/2025/day/5                      #
#                                                                              #
################################################################################
#                                                                              #
# A SOLVED:   2025-12-05 00:45                                                 #
# B SOLVED:   N/A                                                              #
# SOLVER:     friargregarious (greg.denyes@gmail.com)                          #
# HOME:       https://github.com/friargregarious                               #
#                                                                              #
#                   WRITTEN AND TESTED IN PYTHON VER 3.13.7                    #
#                                                                              #
################################################################################
"""

###############################################################################
# imports, globals and helper functions/classes

import os, argparse, toml, sys
import solve_utilities as su
from pathlib import Path
# from random import choices, choice


def data(input_text_path: Path = Path("input.txt")):

    raw = input_text_path.read_text(encoding="UTF-8").split("\n")
    _data = {"fresh": [], "available": []}
    for row in raw:
        if "-" in row:
            _data["fresh"].append(list(map(int, row.split("-"))))
        elif row == "":
            continue
        else:
            _data["available"].append(int(row))

    _data["available"].sort()
    _data["fresh"].sort()

    return _data


###############################################################################
# PART A
###############################################################################

EXAMPLE = {
    1: False,
    5: ["3-5"],
    8: False,
    11: ["10-14"],
    17: ["16-20", "12-18"],
    32: False,
}


def total_fresh(results) -> int:
    return len([x for x in results.values() if x])


def solve_a(source):
    """for solving Part A"""
    print(" Part A ".center(50, "-")) if VERBOSE else None

    results = {}

    for available in source["available"]:
        member_of = []
        for l, h in source["fresh"]:
            if l <= available <= h:
                member_of.append(f"{l}-{h}")

        if not member_of:
            results[available] = False
        else:
            results[available] = member_of

    return total_fresh(results)


###############################################################################
# PART B
###############################################################################


B_EXAMPLES = [[3, 5], [10, 20]]
# B_EXAMPLES = {(3, 5), (10, 20)}

def merge_ranges(L: list, R: list) -> list|bool:
    overlap = max(*L) >= min(*R) or min(*L) >= max(*R)
    if overlap:
        nums = [*L] + [*R] # shove the two ranges together
        return [min(nums), max(nums)] # return the new, merged range
    return overlap

def solve_b(source) -> int:
    """for solving Part B"""
    print("Part B") if VERBOSE else None
    FEEDER = source["fresh"]

    # FRESHES: [[3, 5], [10, 14], [12, 18], [16, 20]]
    print("     EXAMPLE:", B_EXAMPLES) if VERBOSE else None
    print("FRESH RANGES:", FEEDER) if VERBOSE else None

    RUNS = len(FEEDER)
    INDEXES_TO_DELETE = []
    while RUNS > 0:
        INDEXES_TO_DELETE.clear()

        LEFT = FEEDER.pop(0)
        for RIGHT in FEEDER:
            if overlap := merge_ranges(LEFT, RIGHT): 
                LEFT = overlap
                if VERBOSE: 
                    print(f">>>>>>> Merged {LEFT} ({(LEFT[1]-LEFT[0]) +1}) with {RIGHT} ({(RIGHT[1]-RIGHT[0]) +1}) --> {overlap} ({(overlap[1]-overlap[0]) +1})")
                INDEXES_TO_DELETE.append(FEEDER.index(RIGHT))

        old_count = len(FEEDER)
        FEEDER = sorted(
            [x for i, x in enumerate(FEEDER) if i not in INDEXES_TO_DELETE]
            )
        FEEDER.append(LEFT)

        if VERBOSE: 
            print(f"####### FEEDER: ({old_count - len(FEEDER)})\n{FEEDER}")
            

        RUNS -= 1

    TOTAL = sum([HIGH - LOW for LOW, HIGH in FEEDER])

    return TOTAL


###############################################################################
# command line interface
###############################################################################
if __name__ == "__main__":
    os.system("cls")

    # Collect command line arguments
    arguments = argparse.ArgumentParser()
    for arp, ark in su.ARGS_LIST:
        arguments.add_argument(*arp, **ark)
    args = arguments.parse_args()

    su.print_args(vars(args))

    # Load puzzle parameters
    config = toml.load(Path(".env"))

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

        if DO_EXAMPLE:
            f_ex = "(From Example)"
            sp = Path("example_a.txt")
        else:
            f_ex = "(From input)"
            sp = Path("input.txt")

        source_input = data(sp)
        result = solve_a(source_input) if DO_A else solve_b(source_input)

        match f"{'EXPL' if DO_EXAMPLE else 'REAL'}, {p}":
            case "EXPL, A":
                correct_answer = puzzle.examples[0].answer_a
            case "EXPL, B":
                correct_answer = puzzle.examples[0].answer_b
            case "REAL, A":
                correct_answer = puzzle.answer_a if puzzle.answered_a else "unknown"
                config["puzzle"]["answer_a"] = correct_answer
            case "REAL, B":
                correct_answer = puzzle.answer_b if puzzle.answered_b else "unknown"
                config["puzzle"]["answer_b"] = correct_answer
            case _:
                correct_answer = "unknown"

        compare = correct_answer == str(result)
        correct_msg = (
            f"IS {'NOT' if not compare else ''} " f"CORRECT ({correct_answer})"
        )

        su.update_header(puzzle)
        su.save_config(config)

        print(f"Solution ({p}): {result} {correct_msg} {f_ex}")
        os.system("black .")

        if not DO_EXAMPLE:
            su.submit_result(puzzle, result, p, config)
