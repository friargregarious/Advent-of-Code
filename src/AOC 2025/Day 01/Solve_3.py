from aocd import get
import os, toml

# from random import randint
from solve_utilities import Path, print_args
from solve_utilities import argparse
from solve_utilities import clear_screen
from solve_utilities import get_config
from solve_utilities import save_config
from solve_utilities import open_puzzle
from solve_utilities import get_data
from solve_utilities import refresh_readme
from solve_utilities import submit_result
from solve_utilities import Discord


clear_screen()
cfg = get_config()
puzzle = open_puzzle(cfg)
refresh_readme(puzzle)

# data = Path("input.txt").read_text(encoding="utf-8").strip().split("\n")
col = 20


class Pointer:
    def __init__(self, x):
        self.x = x
        self.solve_a = 0
        self.solve_b = 0

    def increment(self):
        self.x += 1
        if self.x > 99:
            self.x -= 100

    def decrement(self):
        self.x -= 1
        if self.x < 0:
            self.x += 100


if __name__ == "__main__":
    arguments = argparse.ArgumentParser()
    arguments.add_argument(
        "-e",
        "--example",
        help="Bool Flag: Test code with example input instead of default 'input.txt'.",
        default=False,
        action="store_true",
    )

    args = arguments.parse_args()
    print_args(args.__dict__)

    if args.example:
        data = get_data(puzzle, example=True).strip().split("\n")
    else:
        data = get_data(puzzle).strip().split("\n")

    this = Pointer(50)

    # turns = [randint(-200, 200) for _ in range(200)]
    turns = [int(x.replace("R", "+").replace("L", "-")) for x in data]

    print(turns)
    for turn in turns:
        print(f"{this.x} + {turn} = {this.x + turn}".rjust(20), end=" | ")
        # if this.x + turn < 0 or this.x + turn > 99:
        #     this.solve_b += 1

        for _ in range(abs(turn)):

            if turn < 0:
                this.decrement()
            else:
                this.increment()

            if this.x == 0:
                this.solve_b += 1

        if this.x == 0:
            this.solve_a += 1

        print(
            f"Position: {this.x:2d} | Part A: {this.solve_a:4d} | Part B: {this.solve_b:4d}"
        )

    # this.solve_b += this.solve_a
    print(" FINAL ".center(20, "-"))
    print(f"Part A: {this.solve_a}")
    print(f"Part B: {this.solve_b}")

    print(" Wrong answers ".center(20, "-"))
    if not puzzle.answered_a:
        submit_result(
            puzzle, this.solve_a, "A", cfg
        )  # report_puzzle(puzzle, this.solve_a, "A")
        # puzzle.answer_a = this.solve_a

    B_TESTS = [
        not this.solve_b in puzzle.submit_results,
        not puzzle.answered_b,
    ]

    if all(B_TESTS):
        submit_result(
            puzzle, this.solve_b, "B", cfg
        )  # report_puzzle(puzzle, this.solve_b, "B")

    save_config(cfg)
    Discord(puzzle=puzzle, config=cfg)
