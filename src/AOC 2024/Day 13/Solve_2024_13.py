"""
################################################################################
#                                                                              #
#                             ADVENT OF CODE: 2024                             #
#                               Claw Contraption                               #
#                     https://adventofcode.com/2024/day/13                     #
#                                                                              #
################################################################################
#                                                                              #
# A SOLVED:   2024-12-13 13:52                                                 #
# SOLVER:     friargregarious (greg.denyes@gmail.com)                          #
# HOME:       https://github.com/friargregarious                               #
#                                                                              #
#                   WRITTEN AND TESTED IN PYTHON VER 3.13.0                    #
#                                                                              #
################################################################################
"""
###############################################################################
# imports, globals and helper functions/classes

import os, argparse, toml, sys
import solve_utilities as su
from pathlib import Path

def data(input_text_path:Path=Path("input.txt"))->dict:
    text_source_list = input_text_path.read_text(encoding="UTF-8").split("\n\n")
    offset = 10_000_000_000_000 if DO_B else 0

    machines = {}
    while len(text_source_list) > 0:
        raw_rows = text_source_list.pop(0).split("\n")
        _, a = raw_rows.pop(0).split(": X+") # button A
        _, b = raw_rows.pop(0).split(": X+") # button B
        _, p = raw_rows.pop(0).split(": X=") # prize
        
        machines[len(machines)] = {
            "a": tuple(map(int,a.split(", Y+"))),
            "b": tuple(map(int,b.split(", Y+"))),
            "prize": tuple( n + offset for n in map(int,p.split(", Y="))),
        }
    return machines
        

###############################################################################
# PART A
###############################################################################
def gen_presses(button, claw, prize):
    index = 0
    x, y = button
    cx, cy = claw
    while button_press((cx + x*index, cy + y*index), claw) <= prize:
        yield index, button_press((cx + x*index, cy + y*index), claw)
        index += 1


def button_press(button, claw):
    return (claw[0] + button[0], claw[1] + button[1])


COST = { "A": 3, "B": 1 }


def solve_machine(this_machine:dict)->list:
    button_a, button_b, prize = this_machine["a"], this_machine["b"], this_machine["prize"]

    prize_x, prize_y = prize
    ax, ay = button_a
    bx, by = button_b

    POSSIBLE_COMBOS = []

    # if just A presses
    if prize_x % ax == 0 and prize_y % ay == 0:
        x_presses = prize_x // ax
        y_presses = prize_y // ay
        
        if x_presses == y_presses:
            POSSIBLE_COMBOS.append((x_presses, 0))

    # if just B presses
    elif prize_x % bx == 0 and prize_y % by == 0:
        x_presses = prize_x // bx
        y_presses = prize_y // by
        
        if x_presses == y_presses:
            POSSIBLE_COMBOS.append((0, x_presses))
        
    else:
        print("Got here")

        # find the lowest common index
        axi = prize_x // ax
        ayi = prize_y // ay
        bxi = prize_x // bx
        byi = prize_y // by


        # avg_index = sum([axi, ayi, bxi, byi]) // 8
        # A_index = avg_index
        # B_index = avg_index
        
        # min_index = min([axi, ayi, bxi, byi]) // 0.8
        
        B_index = 0
        A_index = 0
        
        if bx * 3 > ax and by * 3 > ay:
            COSTEFFECTIVEBUTTON = "B"
            B_index = min((bxi, byi))

        else:
            COSTEFFECTIVEBUTTON = "A"
            A_index = min([axi, ayi])




        # if COSTEFFECTIVEBUTTON == "A":        
        #     A_index = 1 + prize_x // ax // 2
        #     B_index = 0 + prize_x // ax // 20
        # else:
        #     B_index = 1 + prize_x // bx // 2
        #     A_index = 0 + prize_x // ax // 20
        
        while True:
            X:int = (ax * A_index) + (bx * B_index)
            Y:int = (ay * A_index) + (by * B_index)

            print(f"Press A {A_index:,} {"A" if COSTEFFECTIVEBUTTON == "A" else " "}    ", 
                  f"Press B {B_index:,} {"B" if COSTEFFECTIVEBUTTON == "B" else " "}    ", 
                  f"X: {X/prize_x:.4%}".rjust(12), 
                #   f"/{:,}", "    ", 
                  f"Y: {Y/prize_y:.4%}".rjust(12), 
                #   f"/{:,}"
                )

            if X == prize_x and Y == prize_y: POSSIBLE_COMBOS.append((A_index, B_index)); break

            if COSTEFFECTIVEBUTTON == "A":
                if A_index <= 0: break
                elif X > prize_x or Y > prize_y: A_index -= 1
                else: B_index += 1
            else:
                if B_index <= 0: break
                elif X > prize_x or Y > prize_y: B_index -= 1
                else: A_index += 1



    return POSSIBLE_COMBOS


def calc_cost(presses:list)->tuple:
    prices = []

    for presses_a, presses_b in presses:
        tokens = presses_a * COST["A"] + presses_b * COST["B"]
        result = (tokens, presses_a, presses_b)
        
        prices.append(result)

    if len(prices) > 0:
        prices.sort()
        return prices[0]
    
    return (0, 0, 0)


def solve_a(machines):
    """for solving Part A"""
    if DO_B:
        print(" Part B ".center(80, "="))
    else:
        print(" Part A ".center(80, "="))

    machine_prices = {}

    for index, machine in machines.items():

        tokens, apress, bpress = calc_cost( solve_machine(machine) )
        no_combo = apress == bpress == tokens == 0
        if not no_combo:

            print(f"\nMachine #{index} {machine}:")
            machine_prices[index] = tokens
            print(f"\tPresses: A/B {apress}/{bpress}  {apress * COST['A']}+{bpress * COST['B']} = {tokens} Tokens.")

    print(f"\nTotal Tokens: {sum(machine_prices.values())}\n")
    return sum(machine_prices.values())


###############################################################################
# PART B
###############################################################################
def solve_b(machines):
    """for solving Part B"""
    DO_B = True
    return solve_a(machines)


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
        # p = "A" if DO_A else "B"
        
        f_ex = '(From Example)' if DO_EXAMPLE else '(From input)'
        source_input = data( Path("example_a.txt") ) if DO_EXAMPLE else data( Path("input.txt") )
        result = solve_a(source_input) if DO_A else solve_b(source_input)

        correct_msg = ""
        match f"{'EXPL' if DO_EXAMPLE else 'REAL'}, {"A" if DO_A else "B"}":
            # case "EXPL, A": correct_answer = puzzle.examples[0].answer_a
            case "EXPL, A": correct_answer = 480
            case "EXPL, B": correct_answer = puzzle.examples[0].answer_b
            # case "EXPL, B": correct_answer = '34' # puzzle file is corrupt.
            case "REAL, A": correct_answer = puzzle.answer_a if puzzle.answered_a else "unknown"
            case "REAL, B": correct_answer = puzzle.answer_b if puzzle.answered_b else "unknown"
            case _: correct_answer = "unknown"
        
        compare = correct_answer == str(result)
        correct_msg = f"IS CORRECT!! ({correct_answer})" if compare else f"IS NOT CORRECT ({correct_answer})"

        print( f"Solution ({"A" if DO_A else "B"}): {result} {correct_msg} {f_ex}" )
        # if not DO_EXAMPLE: su.submit_result(puzzle, result, p, config)
