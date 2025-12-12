"""
################################################################################
#                                                                              #
#                          ADVENT OF CODE: 2025 DAY 3                          #
#                                    Lobby                                     #
#                     https://adventofcode.com/2025/day/3                      #
#                                                                              #
################################################################################
#                                                                              #
# A SOLVED:   2025-12-03 02:29                                                 #
# B SOLVED:   2025-12-03 04:20                                                 #
# SOLVER:     friargregarious (greg.denyes@gmail.com)                          #
# HOME:       https://github.com/friargregarious                               #
#                                                                              #
#                   WRITTEN AND TESTED IN PYTHON VER 3.13.7                    #
#                                                                              #
################################################################################
"""

###############################################################################
# imports, globals and helper functions/classes

from math import e
import os, argparse, toml, sys
import re
import solve_utilities as su
from pathlib import Path

DO_EXAMPLE, VERBOSE = False, False


def data(input_text_path: Path = Path("input.txt")):
    return input_text_path.read_text(encoding="UTF-8").strip().split("\n")


###############################################################################
# PART A
###############################################################################
def solve_a(source):
    """for solving Part A"""

    print("Part A") if VERBOSE else None

    answers = []
    for row in source:
        _sorted = "".join(sorted(row, reverse=True))

        for biggest in _sorted:
            try:
                max_i = row.index(biggest)
                second = max(row[max_i + 1 :])
                print(row, _sorted, biggest, second, f"Result: {biggest}{second}")
                answers.append(f"{biggest}{second}")
                break
            except:
                continue
    return sum(map(int, answers))


###############################################################################
# PART B
###############################################################################
def solve_b(source):
    """for solving Part B"""
    print("Part B") if VERBOSE else None

    examples = [
        "987654321111",
        "811111111119",
        "434234234278",
        "888911112111",
    ]

    answer, answers = 0, []
    for row in source:
        # print(row)
        bank = list(row)

        while len(bank) > 12:
            print(bank, type(bank), len(bank))

            for i in range(1, len(bank)):
                if bank[i] > bank[i - 1]:
                    del bank[i - 1]
                    break
            else:
                del bank[i]

        new_bank = "".join(bank)
        answers.append(new_bank)
        answer += int(new_bank)

    for r, mine, exmp in zip(bank, answers, examples):
        print(r, len(r), "  <--- Row")
        print(mine, len(mine), "  <--- Mine")
        print(exmp, len(exmp), "  <--- Example", mine == exmp)

    # for row, _s in zip(answers, examples):
    #     print(_s, " <-- Example")
    #     print(row, _s == row, "\n")

    return answer


###############################################################################
# command line interface
###############################################################################
if __name__ == "__main__":
    os.system("cls")

    # Collect command line arguments
    arguments = argparse.ArgumentParser()
    for _args, _kwargs in su.ARGS_LIST:
        arguments.add_argument(*_args, **_kwargs)

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
        result = solve_a(source_input) if DO_A else solve_b(source_input)

        correct_msg = ""
        match f"{'EXPL' if DO_EXAMPLE else 'REAL'}, {p}":
            case "EXPL, A":
                correct_answer = puzzle.examples[0].answer_a
            case "EXPL, B":
                correct_answer = puzzle.examples[0].answer_b
            # case "EXPL, B": correct_answer = '34' # puzzle file is corrupt.
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
        if not DO_EXAMPLE:
            su.submit_result(puzzle, result, p, config)
