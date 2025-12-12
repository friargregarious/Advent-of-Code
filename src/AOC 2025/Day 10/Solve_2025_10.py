"""
################################################################################
#                                                                              #
#                         ADVENT OF CODE: 2025 DAY 10                          #
#                                   Factory                                    #
#                     https://adventofcode.com/2025/day/10                     #
#                                                                              #
################################################################################
#                                                                              #
# A SOLVED:   N/A                                                              #
# B SOLVED:   N/A                                                              #
# SOLVER:     friargregarious (greg.denyes@gmail.com)                          #
# HOME:       https://github.com/friargregarious                               #
#                                                                              #
#                   WRITTEN AND TESTED IN PYTHON VER 3.14.2                    #
#                                                                              #
################################################################################
"""

###############################################################################
# imports, globals and helper functions/classes


import os, argparse, toml, sys
import solve_utilities as su
from decimal import Decimal
from random import choices, randint
from pathlib import Path

VERBOSE = False
banner = "\n" + "*" * 80 + "\n"

def data(input_text_path: Path = Path("input.txt")):
    machines = {}

    ident_text = "The manual describes one machine per line. Each line contains:\n\tA single indicator light diagram in `[`square brackets`]`\n\tOne or more button wiring schematics in `(`parentheses`)`\n\tAnd joltage requirements in `{`curly braces`}`"

    print(banner, ident_text, banner) if VERBOSE else None
    for index, row in enumerate(input_text_path.read_text(encoding="UTF-8").split("\n")):
        items = row.strip().split(" ")
        # print("to parse:", items)
        machine = {
            "line_number": index,

            # [.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}

            "diagram": items[0][1:-1],  # [.###.#] just want the string inside brackets
            # "diagram": [x for x in items[0][1:-1]],  # [.###.#] just want the string inside brackets

            # (0,1,2,3,4)  need list of ints
            # tuple( map(int, (0,1,2,3,4)[1:-1].split(",")) )
            "throws": [tuple( map(int, throws[1:-1].split(",")) ) for throws in items[1:-1]],

            "joltage": list(map(int,items[-1][1:-1].split(","))),
        }

        # {10,11,11,5,10,5} can't use a set, need duplicates
        machines[index]= machine

    if VERBOSE:
        for index, machine in machines.items():
            print(f"Machine #{index:03}:")
            print(f" Diagram: {machine['diagram']}")
            print(f" Buttons: {machine['throws']}")
            print(f" Joltage: {machine['joltage']}")
            print("")

    return machines

class Machine(list):
    index = 0
    def __init__(self, line_number, diagram, throws, joltage):
        super().__init__(diagram)

        Machine.index += 1

        self.name_index = line_number
        self.state = '.' * len(diagram)  # initial state is all off
        self.diagram = diagram
        self.throws = throws
        self.joltage = joltage
        self.sequence_pressed = []

    @property
    def serial(self) -> str:
        return f"Serial #{self.name_index:03}-{Machine.index:04}"

    @property
    def count_pressed(self):
        return len(self.sequence_pressed)

    @property
    def fitness(self) -> Decimal:
        return Decimal(
            sum([
                    1 if s==d else 0 
                    for s, d 
                    in zip(self.state, self.diagram)
                ]) 
                / len(self.diagram)
            ).quantize(Decimal("0.0001"))
    
    def press_button(self, button_index):
        old_state = str(self.state)
        _state = [x=="#" for x in self.state]

        for pos in self.throws[button_index]:
            _state[pos] = not _state[pos]

        self.state = ''.join(['#' if x else '.' for x in _state])
        self.sequence_pressed.append(button_index)

        if VERBOSE:
            msg = (
                f"Machine {self.serial}:\n" 
                f"  Pressed button {self.throws[button_index]}: "
                f"{old_state} -> {self.state}\n"
                f"  Fitness: {self.fitness:0.00%}")
            print(msg)
            
    def __repr__(self) -> str:
        return self.__str__() + f" [Presses: {self.count_pressed:03}] [Fitness: {self.fitness:0.00%}]"

    def __str__(self) -> str:
        return f"Machine {self.serial} ({self.state})"
    

###############################################################################
# PART A
###############################################################################
def solve_a(source):
    """for solving Part A"""
    print("Part A") if VERBOSE else None

    # Machine #000:
    #  Diagram: ..##.#.
    #  Buttons: [
    #       (0, 4), (1, 3, 5), (0, 6), (0, 2, 3, 5), 
    #       (2, 5, 6), (2, 3, 5), (0, 1, 2, 4), (0, 5)
    #       ]
    #  Joltage: [67, 29, 30, 40, 18, 54, 21]

    # diagram indicates machine is on.
    # each machine is initially off. [.......]

    # get each machine into "on" state by pressing buttons.
    # each button toggles certain lights.    0123456      0123456
    # (0, 4) button toggles lights 0 and 4. [.......] -> [#...#..]
    # (1, 3, 5) toggles lights 1, 3, and 5. [#...#..] -> [##.###.]
    # (0, 6) toggles lights 0 and 6.        [##.###.] -> [.#.####]
    # (0, 2, 3, 5)                          [.#.####] -> [#####.#]
    # (2, 5, 6)                             [#####.#] -> [##.##..]
    # (2, 3, 5)                             [##.##..] -> [###.##.]
    # (0, 1, 2, 4)                          [###.##.] -> [.....#.]
    # (0, 5)                                [.....#.] -> [#......]

    # Because none of the machines are running, the joltage requirements are irrelevant and can be safely ignored.
    correct_answers = {}

    def generate_button_combinations(buttons, max_repetitions):
        if max_repetitions == 0:
            return [[]]

        combinations = []
        for button in buttons:
            for sub_combination in generate_button_combinations(buttons, max_repetitions - 1):
                # combinations.append([button] + sub_combination)
                yield [button] + sub_combination

        # return combinations

    for mname, guts in source.items():
        min_presses = -1

        btn_count = len(guts['throws'])
        indexes = [i for i in range(btn_count)]

        for combo in generate_button_combinations(indexes, btn_count+2): 

            # machine = Machine(
            #     diagram ="..##.#.", 
            #     throws  =[(0, 4), (1, 3, 5), (0, 6), (0, 2, 3, 5), 
            #               (2, 5, 6), (2, 3, 5), (0, 1, 2, 4), (0, 5)], 
            #     joltage = [67, 29, 30, 40, 18, 54, 21] 
            #     )

            # populate machine from guts
            print(f"Guts: {guts}") if VERBOSE else None
            machine = Machine(**guts)
            if machine.name_index not in correct_answers: 
                correct_answers[machine.name_index] = []

            for b_index in combo:
                # press a button
                machine.press_button(b_index)

                # check fitness (is it 'ON')?
                if machine.fitness == Decimal("1.0000"):
                    if VERBOSE:
                        print(f"Machine {machine.serial} is correct!")
                    print(machine.__repr__())
    
                    if min_presses < 0: min_presses = machine.count_pressed

                    # if button presses lead to correct answer, store it.
                    correct_answers[machine.name_index].append(len(machine.sequence_pressed))

                    break

            if min_presses > 0 and machine.count_pressed > min_presses: break

            # print(f"Final State: {machine.state} after {machine.count_pressed} presses. \nFitness: {machine.fitness:0.00%} \nSequence: {machine.sequence_pressed}\n")
        print( f"Machine {guts['line_number']} ", min(correct_answers[machine.name_index]))
    print(banner, banner)

    for m, ans in correct_answers.items():
        print(f"Machine {m} Min={min(ans)}  All:", ans)

    import json
    raw = json.dumps({k:min(v) for k, v in correct_answers.items()}, sort_keys=True, indent=4)
    Path("A_Answers.txt").write_text(raw, encoding="UTF-8")

    return sum( min(v) for k, v in correct_answers.items() )



###############################################################################
# PART B
###############################################################################
def solve_b(source):
    """for solving Part B"""
    print("Part B") if VERBOSE else None


    return 0


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
        su.update_header(puzzle)
        os.system("python black .")

        if not DO_EXAMPLE:
            su.submit_result(puzzle, result, p, config)
