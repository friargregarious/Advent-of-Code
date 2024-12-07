"""
################################################################################
#                                                                              #
#                             ADVENT OF CODE: 2024                             #
#                                Bridge Repair                                 #
#                     https://adventofcode.com/2024/day/7                      #
#                                                                              #
################################################################################
#                                                                              #
# A SOLVED:   2024-12-07 10:39                                                 #
# B SOLVED:   2024-12-07 10:39                                                 #
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
import sys
import solve_utilities as su
from pathlib import Path

def data(input_text_path:Path=Path("input.txt")):
    data = []

    for row in input_text_path.read_text(encoding="UTF-8").split("\n"):
        answer, values = row.split(": ")
        # print(f"First split: {answer} and {values}") if VERBOSE else None
        equa = {
            "answer" : int(answer),  
            "values" : list(map(int, values.split(" ")))
            }

        data.append(equa)
        
    return data


###############################################################################
# PART A
###############################################################################
def solve_a(data):
    """for solving Part A"""
    ops = ("+", "*")

    working_results = []
    for r in data:
        # print(f"r -> {r}") if VERBOSE else None
        ans = r["answer"]
        vals = r["values"]

        bit_str = "1" * (len(vals) - 1)
        possible = [bin(i)[2:].rjust(len(bit_str), "0").replace("0", ops[0]).replace("1", ops[1])  for i in range(int(bit_str, 2) + 1)]
        results = []
        for eq in possible:
            equation = [ str(vals[0]) ] + [ f" {op} {val}" for op, val in zip(eq, vals[1:]) ]
            # print("".join(equation)) if VERBOSE else None
            # print(f"Equation: {equation}")

            result = 0
            running = int(equation[0])
            for x in equation[1:]:
                result = eval(f"{running}{x}")
                # print(f"{running}{x} =", result)
                running = result

            good_result = result == ans
            
            if good_result:
                print(f"Equation: {''.join(equation)} | Result: {result} = Answer: {ans} --> {result == ans}")
                results.append(good_result)

        if any(results):
            working_results.append(ans)
         
    return sum(working_results)


###############################################################################
# PART B
###############################################################################
def solve_b(data):
    """for solving Part B"""

    def int_b3(n:int)->str:
        """convert integer to base 3"""
        sign = '-' if n < 0 else ''
        n = abs(n)
        s = ''
        while n != 0:
            s = str(n % 3) + s
            n = n // 3
        return str(sign + s)


    def b3_int(s:str)->int:
        """convert base 3 to integer"""
        ans = 0
        for c in map(int, s):
            ans = 3 * ans + c
        return ans

    ops = ("+", "*", "|")
    working_results = []


    for r in data:
        # print(f"r -> {r}") if VERBOSE else None
        ans = r["answer"]
        vals = r["values"]

        bit_str = "2" * (len(vals) - 1)
        possible = [
            int_b3(i).rjust(len(bit_str), "0").replace("0", ops[0]).replace("1", ops[1]).replace("2", ops[2])
            for i in range(b3_int(bit_str) + 1)
            ]
        results = []

        for eq in possible:
            equation = [ str(vals[0]) ] + [ f" {op} {val}" for op, val in zip(eq, vals[1:]) ]

            result = 0
            running = int(equation[0])
            for x in equation[1:]:
                if "|" not in x:
                    result = eval(f"{running}{x}")
                else:
                    result = int(
                        str(running) + x.strip("| ")
                    )
                
                running = result

            good_result = result == ans
            
            if good_result:
                print(f"Equation: {''.join(equation)} | Result: {result} = Answer: {ans} --> {result == ans}")
                results.append(good_result)

        if any(results):
            working_results.append(ans)
         
    return sum(working_results)




    return 0


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

        print( f"Solution ({p}): {result} {f_ex}" )
        su.submit_result(puzzle, result, p, config)


