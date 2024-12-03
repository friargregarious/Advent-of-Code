# python 3.13 - utf-8
## advent of code 2015 day 7
## https://adventofcode.com/2015
## coder Greg Denyes
#             - friargrearious@gmail.com
#             - greg.denyes@gmail.com

import decimal

from click import Path
import toml
import solve_utils

cfg = solve_utils.load_cfg()
log = []

###### HELPERS ###############################################################

def AND_OR(data_line, ans, instructions):
    # at AND az -> bb
    # 44 AND 12 -> 234
    # x OR ai -> aj
    # 3 OR 43 -> 23

    a, _CMD, b, _, target = data_line.split(" ")

    send_back = False

    if a.isnumeric():
        a = int(a, base=10)
    elif a in ans:
        a = ans[a]
    else:
        send_back = True

    if b.isnumeric():
        b = int(b, base=10)
    elif b in ans:
        b = ans[b]
    else:
        send_back = True

    if send_back:
        instructions.append(f"{a} AND {b} -> {target}")
        return "Throw back"

    if _CMD == "AND":
        #     0101 (decimal 5)
        # AND 0011 (decimal 3)
        #   = 0001 (decimal 1)
        c = a & b

    else:  # _CMD == "OR":
        #     0101 (decimal 5)
        #  OR 0011 (decimal 3)
        #   = 0111 (decimal 7)
        c = a | b

    ans[target] = c
    log.append(f"{a} {_CMD} {b} -> {target} = {c}")
    # print(ans[target])
    # return ans[target]



def PUT_NOT(data_line, ans, instructions):

    if "NOT" in data_line:
        _, subject, _, target = data_line.split(" ")
    else:
        subject, _, target = data_line.split(" ")

    if subject.isnumeric():
        subject = int(subject)
    elif subject in ans:
        subject = ans[subject]
    else:
        instructions.append(data_line)
        return "Throw back"

    if "NOT" in data_line:
        #    0101 (decimal 5)
        # NOT
        #  = 1010 (decimal 10)

        a = ("0" * 16 + bin(subject)[2:])[-16:]
        b = "0b"
        for i in a:
            if i == "1":
                b += "0"
            else:
                b += "1"
        
        ans[target] = int(b, base=2)
        log.append(f"NOT {subject} -> {target} = {ans[target]}")

    else:  # "PUT"
        ans[target] = subject
        log.append(f"{subject} -> {target} = {subject}")
    # print(ans[target])

def SHIFT(data_line: str, ans: dict, instructions: list):
    # dt LSHIFT 15 -> dx
    # hz RSHIFT 2 -> ia

    subject, _shift, positions, _, target = data_line.split(" ")

    if subject.isnumeric():
        subject = int(subject, base=10)
    elif subject in ans:
        subject = ans[subject]
    else:
        instructions.append(data_line)
        return "Throw back"

    pos = int(positions)
    to_shift = bin(subject)[2:].rjust(16, "0")
    
    if _shift == "RSHIFT":
        #    01110000 (decimal 5)
        # RSHIFT 2
        #  = 00011100 (decimal 1)
        # subject >>= pos
        temp = to_shift[:-pos].rjust(16, "0")
        subject = int(temp, base=2)

    else:  # if _shift == "LSHIFT":
        #    00000101 (decimal 5)
        # LSHIFT 3
        #  = 00101000 (decimal 10)
        # subject <<= pos
        temp = to_shift[pos:].ljust(16, "0")
        subject = int(temp, base=2)

    ans[target] = subject
    # log.append(f"Shifted {to_shift} {_shift} by {pos} positions to {temp} int value is {subject}")
    log.append(f"{data_line.split(' ')[0]} {_shift} {pos} -> {target} = {subject}")
    # print(ans[target])
    # return ans[target]


def parse_input(input_file):
    x = solve_utils.Path(input_file).read_text(encoding="utf-8").splitlines()

    if isinstance(x, list):
        return x
    else:
        raise Exception("Not a list")


###### PARTS #################################################################
def part1(instructions):
    total_instructions = len(instructions)

    answers = {}
    while len(instructions) > 0:
        x = instructions.pop(0)

        if ("AND" in x) or ("OR" in x):
            print(AND_OR(x, answers, instructions))

        elif "SHIFT" in x:
            print(SHIFT(x, answers, instructions))

        else:  # PUT: lx -> a    NOT: NOT ax -> ay
            print(PUT_NOT(x, answers, instructions))

        if len(instructions) > 0:
            completed = total_instructions - len(instructions)
            print(f"Completed: {completed/total_instructions:2.2%}")
        else:
            print(f"Completed: 100%")

    _a = sorted(answers.keys())
    answers = {a: answers[a] for a in _a}    
    return answers


def part2(data):
    pass


###### RUNNERS ###############################################################
def main(args):
    # using example or regular input ######################################
    if args.example:
        source = parse_input("example_input.txt")
        return part1(source), None
    else:
        source = parse_input("input.txt")

    # solve for a, b or both ##############################################
    if args.part == 1:
        part_1 = part1(source)
        answer = (part_1, None)
    elif args.part == 2:
        part_2 = part2(source)
        answer = (None, part_2)
    else:
        part_1 = part1(source)
        part_2 = part2(source)
        answer = (part_1, part_2)

    return answer



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-e",
        "--example",
        help="Run This Solve on example input. Default is regular input.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-p",
        "--part",
        help="Which part to run, 1 or 2. Default is both 1 then 2.",
        action="store",
        type=int,
        default=0,
    )
    args = parser.parse_args()

    a, b = main(args)

    if args.example:
        solve_utils.Path("example_output.toml").write_text(toml.dumps(a))
    elif args.part == 1:
        solve_utils.Path("part1_output.toml").write_text(toml.dumps(a))
        print("**** RESULTS ****\n", "\n".join(log))
        
    elif args.part == 2:
        solve_utils.Path("part2_output.toml").write_text(toml.dumps(b))
    else:
        solve_utils.Path("part1_output.toml").write_text(toml.dumps(a))
        solve_utils.Path("part2_output.toml").write_text(toml.dumps(b))
        
    if isinstance(a, dict):
        print(f"Found {sum([1 for x in a.values() if x > 0])} values in {len(a)} answers.")
        if a["a"] > 0:
            print(f"SUCCESS: Part 1: {a['a']}")
        else:
            print(f"FAILURE: Part 1: {a['a']}")