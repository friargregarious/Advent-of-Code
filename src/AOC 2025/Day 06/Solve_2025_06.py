"""
################################################################################
#                                                                              #
#                          ADVENT OF CODE: 2025 DAY 6                          #
#                               Trash Compactor                                #
#                     https://adventofcode.com/2025/day/6                      #
#                                                                              #
################################################################################
#                                                                              #
# A SOLVED:   N/A                                                              #
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

# from tools import Path
import os
import math
from pathlib import Path
VERBOSE = True

###############################################################################
# PART A
###############################################################################

def data(input_path: Path):

    step1 = input_path.read_text(encoding="UTF-8")
    # print(step1) if VERBOSE else None

    while "  " in step1:
        step1 = step1.replace("  ", " ")

    # if VERBOSE:
    #     print("SHORTENED SPACES")
    #     print(step1)

    step2 = []
    for row in step1.split("\n"):
        step2.append(row.split())

    # if VERBOSE:
    #     print("split lines")
    #     for r in step2:
    #         print(r)

    grouped = list(zip(*step2))
    # print("*" * 30 + "\n", grouped) if VERBOSE else None

    return grouped
def solve_a(source):
    """for solving Part A"""
    print("Part A") if VERBOSE else None

    examples = [33210, 490, 4243455, 401]
    example = sum(examples)
    assert 4277556 == example

    # source = data(Path("example_a.txt") )
    source = data(Path("input.txt"))
    results = []
    for vals in source:
        print(vals)
        nums = [int(x) for x in vals[:-1]]
        result = math.prod(nums) if vals[-1] == "*" else sum(nums)
        results.append(result)
        print(result) if VERBOSE else None

    return sum(results)


###############################################################################
# PART B
###############################################################################
GROUP_COUNTS = 0

def data_2(input_path: Path):
    step1 = input_path.read_text(encoding="UTF-8").split("\n")
    global GROUP_COUNTS 
    GROUP_COUNTS = step1[-1].count("*") + step1[-1].count("+")
    return step1

example_b = [
    [('123', '45' , '6', "*"), '33210'],
    [( '328' + '64' + '98', "+") , '490'],
    [( '51' , '387' , '215', "*") , '4243455'],
    [( '64' + '23' + '314', "+") , '401'],
]

def solve_b(source):
    """for solving Part B"""
    print("Part B") if VERBOSE else None

    nums = []
    group = []
    sym = None
    total = 0
    for row in [x for x in zip(*source)][::-1]:
        
        if all( [ x==" " for x in row] ):
            found_nums = "".join([str(x).rjust(6) for x in group[:-1]]).rjust(40)
            sub_ans = sum(group[:-2]) if group[-2]=="+" else math.prod(group[:-2])
            pre_cal = group[-1]
            print("group complete:", found_nums, sub_ans == pre_cal,  str(pre_cal).rjust(15), sub_ans )
            group.clear()
            total += sub_ans
            continue

        val = "".join(row[:-1])
        sym = row[-1]

        group.append(int(val))
        if sym == "+":
            group.extend([sym, sum(map(int, group)) ] ) 
            nums.append(group)

        elif sym == "*":
            group.extend([sym, math.prod(map(int, group)) ] )
            nums.append(group)
        

    for row in nums:
        print(row[:1])

    answers = [sum(row[:-2]) if row[-2]=="+" else math.prod(row[:-2]) for row in nums]
    # print(answers)
    print(f"Total: {total} == {sum(answers)}")
    # print(sum(answers))
    return sum(answers)


###############################################################################
# command line interface
###############################################################################
if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    # arguments = argparse.ArgumentParser()

    # DO_A, DO_B, DO_EXAMPLE, VERBOSE, SUBMIT = build_args_list(arguments)
    # PUZZLE = open_puzzle(INI)
    # DATA = data(Path(get_DATA(DO_EXAMPLE)))
    # DONE_A, DONE_B = PUZZLE.answered_a, PUZZLE.answered_b

    # print(build_submit_msg(DO_A, DO_EXAMPLE, SUBMIT))

    # do_submit()
    # print(f"A:", solve_a(data(Path("input.txt"))))

    
    mysolvebe = solve_b(data_2(Path("example_a.txt")))
    mysolveb = solve_b(data_2(Path("input.txt")))

    print(f"B Example:", mysolvebe, 4277556, mysolveb==4277556 )
    print(f"B  Actual:", mysolveb)

