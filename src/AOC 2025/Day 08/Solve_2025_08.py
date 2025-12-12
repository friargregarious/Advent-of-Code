"""
################################################################################
#                                                                              #
#                          ADVENT OF CODE: 2025 DAY 8                          #
#                                  Playground                                  #
#                     https://adventofcode.com/2025/day/8                      #
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


from decimal import Decimal
import os, argparse, toml, sys
import itertools
import solve_utilities as su
from pathlib import Path
from colorama import Fore, Style


def orange(text) -> str:
    return f"{Fore.LIGHTYELLOW_EX}{text}{Style.RESET_ALL}"


def red(text) -> str:
    return f"{Fore.LIGHTRED_EX}{text}{Style.RESET_ALL}"


def green(text) -> str:
    return f"{Fore.LIGHTGREEN_EX}{text}{Style.RESET_ALL}"


def data(input_text_path: Path = Path("input.txt")):
    text_source_list = input_text_path.read_text(encoding="UTF-8").split("\n")

    return [tuple(x for x in map(int, row.split(","))) for row in text_source_list]


def euclidean_distance(point_a, point_b) -> float:
    """
    This method calculates the Euclidean distance between two points. It takes two points of arbitrary dimension as input and returns the Euclidean distance between them.

    Parameters
    ----------
    point_a : tuple
        The first point to calculate the distance from.

    point_b : tuple
        The second point to calculate the distance from.

    Returns
    -------
    float
        The Euclidean distance between the two points.
    """
    # this method doesn't require a strict count of dimensions
    return Decimal(sum((a - b) ** 2 for a, b in zip(point_a, point_b)) ** 0.5).quantize(
        Decimal("0.0000001")
    )


def curcuit_length(chain: list) -> float:
    try:
        return round(sum([x.distance for x in chain]), 4)
    except Exception as e:
        print(red(f"Error: {e}"))
        print(f"Parameter Passed (Type: {type(chain)}):", chain)
        raise e


class Connector:
    def __init__(self, point_a, point_b):
        a_is_Tup = isinstance(point_a, tuple)
        b_is_Tup = isinstance(point_b, tuple)

        if all([a_is_Tup, b_is_Tup]):
            self.left_junction = point_a
            self.right_junction = point_b
            self.distance = euclidean_distance(point_a, point_b)
            return None

        elif not a_is_Tup:
            # Raise TypeError with a specific, informative message
            msg = f"Invalid data type: expected 'Tuple' but received '{type(point_a).__name__}'. Point 'A' must be a Tuple for processing."

        elif not b_is_Tup:
            # Raise TypeError with a specific, informative message
            msg = f"Invalid data type: expected 'Tuple' but received '{type(point_b).__name__}'. Point 'B' must be a Tuple for processing."

        raise TypeError(msg)

    def __repr__(self):
        return orange(f"<-{self.left_junction}-@-{self.right_junction}->")

    def __str__(self):
        return green(
            (
                f"({self.left_junction}".rjust(16)
                + f" <- {self.distance:.4f} -> "
                + f"{self.right_junction})".ljust(16)
            ).center(55)
        )

    def __add__(self, other):
        # if this method is called, it is because this object is on the left of the == expression (because )
        if self != other:
            raise ValueError("Other left_Junction does not match this right_junction.")

        if isinstance(other, Connector):
            if self.right_junction == other.left_junction:
                return [self, other]
            else:
                return [other, self]

        elif isinstance(other, list):
            if isinstance(other[0], Connector):
                if self.right_junction == other[0].left_junction:
                    return [self] + other

                elif self.left_junction == other[-1].right_junction:
                    return other + [self]
            else:
                return NotImplemented

        else:
            # Raise TypeError with a specific, informative message
            msg = f"Invalid data type: expected 'Connector' or 'List[Connector,]' but received '{type(other).__name__}'. Data must be a Connector for processing."
            raise TypeError(msg)

    def __eq__(self, other):
        # if this method is called, it is because this object is on the left of the == expression
        if isinstance(other, Connector):
            return self.right_junction == other.left_junction
        elif isinstance(other, list):
            if isinstance(other[0], Connector):
                return self.right_junction == other[0].left_junction
            else:
                # Raise TypeError with a specific, informative message
                msg = f"Invalid data type: expected 'Connector' but received '{type(other[0]).__name__}'. Data must be a Connector for processing."
        else:
            # Raise TypeError with a specific, informative message
            msg = f"Invalid data type: expected 'Connector' but received '{type(other).__name__}'. Data must be a Connector for processing."
        raise TypeError(msg)

    def __lt__(self, other):
        if isinstance(other, Connector):
            return self.distance < other.distance
        else:
            # Raise TypeError with a specific, informative message
            msg = f"Invalid data type: expected 'Connector' but received '{type(other).__name__}'. Data must be a Connector for processing."
            raise TypeError(msg)

    def __gt__(self, other):
        if isinstance(other, Connector):
            return self.distance > other.distance
        else:
            # Raise TypeError with a specific, informative message
            msg = f"Invalid data type: expected 'Connector' but received '{type(other).__name__}'. Data must be a Connector for processing."
            raise TypeError(msg)

    def __le__(self, other):
        if isinstance(other, Connector):
            return self.__gt__(other) or self.__eq__(other)
        else:
            # Raise TypeError with a specific, informative message
            msg = f"Invalid data type: expected 'Connector' but received '{type(other).__name__}'. Data must be a Connector for processing."
            raise TypeError(msg)

    def __ge__(self, other):
        if isinstance(other, Connector):
            return self.__lt__(other) or self.__eq__(other)
        else:
            # Raise TypeError with a specific, informative message
            msg = f"Invalid data type: expected 'Connector' but received '{type(other).__name__}'. Data must be a Connector for processing."
            raise TypeError(msg)


###############################################################################
# PART A
###############################################################################
def solve_a(source):
    """for solving Part A"""
    print("Part A") if VERBOSE else None

    connections = sorted(
        [[point_a, point_b] for point_a, point_b in itertools.combinations(source, 2)],
        key=lambda x: euclidean_distance(*x),
    )

    log = [su.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")]

    log.append(f"Start with {len(connections)} connections.")

    for x in connections:
        log.append(x)

    final_chains = []
    while len(connections) > 0:
        this_chain = connections.pop(0)
        log.append(f"Starting chain with: {this_chain}")
        connectable = 100
        while connectable > 0:

            # clear out all the duplicate junctions
            left = this_chain[0]
            right = this_chain[-1]

            previous_connections = len(connections)
            connections = sorted(
                [
                    junc
                    for junc in connections
                    if not any([junc[0] == left, junc[1] == right])
                ],
                key=lambda x: euclidean_distance(*x),
            )

            log.append(
                f"Removed {previous_connections - len(connections)} duplicates.  {len(connections)} left."
            )

            # find all the connections that fit
            can_connect = sorted(
                [junc for junc in connections if junc[0] == right or junc[1] == left],
                key=lambda x: euclidean_distance(*x),
            )

            connectable = len(can_connect)

            # add the shortest possibility to the chain
            if connectable > 0:
                to_connect = can_connect[0]
                if to_connect[0] == this_chain[-1]:
                    this_chain += [to_connect[1]]

                if to_connect[1] == this_chain[0]:
                    this_chain = [to_connect[0]] + this_chain

            else:
                log.append("No more connections to add.")
        # there are no more connections that fit the current chain
        else:
            chain_text = " -> ".join([str(x) for x in this_chain])
            log.append(f"Archive this Chain: { chain_text }")
            final_chains.append(this_chain)

    log.append(f"Found {len(final_chains)} chains.")

    for x in log:
        print(x)

    Path("log.txt").write_text("\n".join(map(str, log)), encoding="utf-8")

    for chain in final_chains:
        print(chain)

    return 0


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
        os.system("black .")

        if not DO_EXAMPLE:
            su.submit_result(puzzle, result, p, config)
