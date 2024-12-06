"""
################################################################################
#                                                                              #
#                             ADVENT OF CODE: 2024                             #
#                                 Print Queue                                  #
#                     https://adventofcode.com/2024/day/5                      #
#                                                                              #
################################################################################
#                                                                              #
# A SOLVED:   2024-12-05 01:09                                                 #
# B SOLVED:   2024-12-05 10:55                                                 #
# SOLVER:     friargregarious (greg.denyes@gmail.com)                          #
# HOME:       https://github.com/friargregarious                               #
#                                                                              #
#                   WRITTEN AND TESTED IN PYTHON VER 3.13.0                    #
#                                                                              #
################################################################################
"""
###############################################################################
# imports, globals and helper functions/classes

import os, argparse, toml, json
import solve_utilities as su
from pathlib import Path
from time import sleep
from markdownify import markdownify

def data(input_text_path:Path=Path("input.txt")):
    raw_rules, raw_updates = input_text_path.read_text(encoding="UTF-8").split("\n\n")

    rules = raw_rules.split("\n")
    updates = [row.split(",") for row in raw_updates.split("\n")]

    return {"rules" : rules, "updates" : updates}


###############################################################################
# PART A
###############################################################################
def solve_a(source:dict):
    """for solving Part A"""
    rules = source["rules"]
    updates = source["updates"]

    ordered = []
    disordered = []
        
    for update in updates:
        rules_passed = []
        working_rules = [] 
        for r in rules:
            x, y = r.split("|")
            if x in update and y in update: working_rules.append(r)
        
        for rule in working_rules:
            before, after = rule.split("|")
            before_index = update.index(before)
            after_index = update.index(after)
            
            # print("rule:", rule, "update:", update, before_index < after_index)
            rules_passed.append( before_index < after_index )

        # print("rules passed:", rules_passed, all(rules_passed))
        if all(rules_passed) and len(rules_passed) > 0:
            ordered.append(update)
        else:
            disordered.append(update)
    
    middle_sum = 0
    for update in ordered:
        # print("vetted update:", update)
        middle_sum += int( update[int(len(update) // 2)] )

    # Path("disordered.json").write_text(json.dumps(disordered))
    return middle_sum


###############################################################################
# PART B
###############################################################################
def solve_b(source):
    """for solving Part B"""
    rules = source["rules"]
    updates = source["updates"]

    ordered = []
    disordered = []
        
    for update in updates:
        rules_passed = []
        working_rules = [] 
        for r in rules:
            x, y = r.split("|")
            if x in update and y in update: working_rules.append(r)
        
        for rule in working_rules:
            before, after = rule.split("|")
            before_index = update.index(before)
            after_index = update.index(after)
            
            # print("rule:", rule, "update:", update, before_index < after_index)
            rules_passed.append( before_index < after_index )

        # print("rules passed:", rules_passed, all(rules_passed))
        if all(rules_passed) and len(rules_passed) > 0:
            # ordered.append(update)
            pass
        else:
            disordered.append(update)

    # reordering the messes
    for update in disordered:
        working_rules = [] 
        for r in rules:
            x, y = r.split("|")
            if x in update and y in update: working_rules.append(r)

        # pages = update.split(",")
        passed_rules = []
        while len(working_rules) > 0:
            rule = working_rules.pop()

            # print(working_rules, type(working_rules))
            # print(rule, type(rule), before, after)
            before, after = rule.split("|")
            before_index = update.index(before)
            after_index = update.index(after)

            # print("rule:", rule, "update:", update, before_index < after_index)
            if before_index > after_index:  # Failed tests, reset all tests
                working_rules += [rule] + passed_rules
                passed_rules.clear()

                update.append(update.pop(after_index))
                # print(f"moved {after} to the end")
            else:
                passed_rules.append(rule)

        # print(f"fixed: {update}")
        ordered.append(update)

    middle_sum = 0
    for update in ordered:
        # print("vetted update:", update)
        middle_sum += int( update[int(len(update) // 2)] )



    return middle_sum


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

    if DISCORD:
        su.send_discord(config, puzzle)
    
    if REFRESH:
        su.refresh_readme(puzzle)

    # Setup input data
    if DO_EXAMPLE and DO_A:
        result = solve_a(data(Path("example_a.txt")))
        print(f"Part A From Example: {result}")
    elif DO_EXAMPLE and DO_B:
        result = solve_b(data(Path("example_a.txt")))
        print(f"Part B From Example: {result}")
    else:
        source_input = data(Path("input.txt"))
        if DO_A:
            result = solve_a(source_input)
            print(f"Part A From Input: {result}")
        else:
            result = solve_b(source_input)
            print(f"Part B From Input: {result}")

    if SUBMIT_PUZZLE:
        p = "A" if DO_A else "B"
        su.submit_result(puzzle, result, p, _puzzle_path)
