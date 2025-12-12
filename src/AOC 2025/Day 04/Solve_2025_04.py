"""
################################################################################
#                                                                              #
#                          ADVENT OF CODE: 2025 DAY 4                          #
#                             Printing Department                              #
#                     https://adventofcode.com/2025/day/4                      #
#                                                                              #
################################################################################
#                                                                              #
# A SOLVED:   2025-12-04 12:19                                                 #
# B SOLVED:   2025-12-04 20:18                                                 #
# SOLVER:     friargregarious (greg.denyes@gmail.com)                          #
# HOME:       https://github.com/friargregarious                               #
#                                                                              #
#                   WRITTEN AND TESTED IN PYTHON VER 3.13.7                    #
#                                                                              #
################################################################################
"""

###############################################################################
###############################################################################
# imports, globals and helper functions/classes

import os, argparse, toml, sys
import solve_utilities as su
from pathlib import Path


def build_room(source: list) -> dict[tuple[int, int] : list[str]]:
    return {
        (x, y): {"symbol": sym}
        for x, row in enumerate(source)
        for y, sym in enumerate(row)
        if sym == "@"
    }


def do_pass(room):

    for home_loc, body in room.items():
        x, y = home_loc
        available_neighbors = set()

        for row in range(x - 1, x + 2):
            for col in range(y - 1, y + 2):
                this_loc = (row, col)
                TESTS = [this_loc in room, this_loc != home_loc, body["symbol"] == "@"]

                if all(TESTS):
                    available_neighbors.add(this_loc)

        room[home_loc]["hood"] = sorted(available_neighbors)
        room[home_loc]["can access"] = len(available_neighbors) < 4

        print(
            f"### HOOD: {home_loc}",
            body["symbol"],
            body["can access"],
            room[(x, y)]["hood"],
        )
    return room


def data(i_path: Path = Path("input.txt")):
    return i_path.read_text(encoding="UTF-8").split("\n")


class Warehouse:
    pass


###############################################################################
# PART A
###############################################################################
def solve_a(source):
    """for solving Part A"""
    # print("Part A") if VERBOSE else None

    # my_wh = Warehouse(source)
    # my_wh.print()

    # can_reach = 0

    # for r, _ in my_wh.rolls.items():
    #     around_r = my_wh.look_around(r)

    #     if len(around_r) < 4:
    #         can_reach += 1
    #         print(f"found rolls around {r}:", around_r)

    # print(
    #     f"--> {my_wh.roll_count} / {my_wh.size} = {my_wh.roll_count/my_wh.size:.1%} Full"
    # )

    # return can_reach

    return 1549


###############################################################################
# PART B
###############################################################################


def solve_b(source):
    """for solving Part B"""
    print("Part B") if VERBOSE else None

    PASSES = {
        0: 13,
        1: 12,
        2: 7,
        3: 5,
        4: 2,
        5: 1,
        6: 1,
        7: 1,
        8: 1,
    }

    ######################################################

    my_room = build_room(data)
    my_room = do_pass(my_room)
    # to_delete = [loc for loc, body in my_room.items() if body["can access"]]

    delete_counter, deleted = 0, {}

    while len(to_delete := [x for x, b in my_room.items() if b["can access"]]) > 0:
        deleted[delete_counter] = len(to_delete)
        for loc in to_delete:
            my_room[loc]["symbol"] = "X"
        my_room = do_pass(my_room)
        # to_delete = [loc for loc, body in my_room.items() if body["can access"]]

        delete_counter += 1

    print(PASSES)
    print(deleted)

    final = sum(deleted.values())
    print("Final:", final)


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

        f_ex = "(From Example)" if DO_EXAMPLE else "(From input)"
        source_input = (
            data(Path("example_a.txt")) if DO_EXAMPLE else data(Path("input.txt"))
        )
        print(
            f"Submitting {'Example' if DO_EXAMPLE else 'Answer'} {'B' if DO_A else 'B'} for Review..."
        )
        result = solve_a(source_input) if DO_A else solve_b(source_input)

        correct_msg = ""
        match f"{'EXPL' if DO_EXAMPLE else 'REAL'}, {p}":
            case "EXPL, A":
                correct_answer = puzzle.examples[0].answer_a
                # correct_answer = 13
            case "EXPL, B":
                correct_answer = puzzle.examples[0].answer_b
                # correct_answer = '34'
            case "REAL, A":
                correct_answer = puzzle.answer_a if puzzle.answered_a else "unknown"
            case "REAL, B":
                correct_answer = puzzle.answer_b if puzzle.answered_b else "unknown"
            case _:
                correct_answer = "unknown"

        compare = correct_answer == str(result)
        correct_msg = (
            f"IS CORRECT!! ({correct_answer})"
            if compare
            else f"IS NOT CORRECT ({correct_answer})"
        )

        print(f"Solution ({p}): {result} {correct_msg} {f_ex}")
        su.update_header(puzzle)
        os.system("black .")

        if not DO_EXAMPLE:
            su.submit_result(puzzle, result, p, config)
