"""
#             ADVENT OF CODE | 2023 | PULSE PROPAGATION | PART [A]            #
#                         adventofcode.com/2023/day/20                        #
# SOLVER: --------------------------------------------------- friargregarious #
# CONTACT: --------------------------------------- friar.gregarious@gmail.com #
# HOME: -------------------------------------------------------------- github #
# SOURCE: ---------------------------------- ~/Advent-of-Code/AOC 2023/Day 20 #
# WRITTEN AND TESTED IN: --------------------------------------------- 3.11.6 #
"""
###############################################################################
# IMPORTS #####################################################################
###############################################################################

import os
from operator import itemgetter
from pyclbr import Class

from numpy import sign

#  from my_utilities import MyConfigParser as MyCfg
import my_utilities

import math

# from datetime import datetime
# from termcolor import colored
# import aocd

###############################################################################
# DECLARATIONS ################################################################
###############################################################################

__version__ = "0.0.44"
__example_answer_1__ = 32000000
__example_answer_2__ = 11687500
__run_on_example__ = False
YEAR, DAY = 2023, 20

###############################################################################
# GATHER_TOOLS ################################################################
###############################################################################
OFF, ON, HIGH, LOW = False, True, 1, 0


class Node:
    pulses = {HIGH: 0, LOW: 0}

    def push(self):
        self.pulses[LOW] += 1
        return [{"src": "Button", "signal": LOW, "tgt": "broadcaster"}]


class OutPut(Node):
    def __init__(self, name: str, targets: list) -> None:
        self.name = name

    def process(self, msg):
        rec_sig = "LOW"

        if msg["signal"]:
            rec_sig = "HIGH"

        print(f"{self.name} received: -{rec_sig}-")
        return []


class FlipFlop(Node):
    """Flip-flop modules (prefix %) are either on or off;
    they are initially off.
    """

    def __init__(self, name, targets: list) -> None:
        self.name = name
        self.state = OFF  # OFF = False, ON = True
        self.targets = targets  # targets can contain 1 or more elements

    def __str__(self) -> str:
        st_str = "OFF"
        if self.state:
            st_str = "ON"

        return f"FF ({self.name}): ({st_str}) -> {', '.join(self.targets)} "

    def process(self, msg: dict):
        """
        However, if a flip-flop module receives a low pulse,
        it flips between on and off.
        > If it was off, it turns on and sends a high pulse.
        > If it was on, it turns off and sends a low pulse.
        """
        if VERBOSE:
            print(f"{self.name} received:".center(80, "-"))
            print(f"{msg}".center(80))

        signal = msg["signal"]
        bundle = []

        if signal == LOW:  # rcv "LOW"
            # if a flip-flop module receives a low pulse,
            # it flips between on and off.
            self.state = not self.state

            if self.state:
                # If it was off, it turns on and sends a high pulse.
                out_sig = HIGH  # if it is now 'ON'
            else:
                # If it was on, it turns off and sends a low pulse.
                out_sig = LOW  # if it is now 'OFF'

            for target in self.targets:
                bundle.append({"src": self.name, "signal": out_sig, "tgt": target})

        for line in bundle:
            self.pulses[line["signal"]] += 1

        # If a flip-flop module receives a high pulse, it is ignored
        if VERBOSE:
            print(f"returning: {bundle}".center(80))
        return bundle


class Conjunction(Node):
    def __init__(self, name, targets) -> None:
        """
        Conjunction modules (prefix &) remember the type of the most
        recent pulse received from each of their connected input modules
        """
        self.targets = targets
        self.inputs = {}
        self.name = name

    @property
    def all_high(self):
        """Are all inputs remembered as high pulses?"""
        return "LOW" not in list(self.inputs.values())

    def __str__(self) -> str:
        in_str = "No Inputs"
        if len(self.inputs) > 0:
            inputs_list = [f"{key}:{val}" for key, val in self.inputs.items()]
            in_str = ", ".join(inputs_list)

        return f"CJ ({self.name}): [{in_str}] -> {', '.join(self.targets)}"

    def process(self, msg: dict):
        """When a pulse is received, the conjunction module first updates its
        memory for that input."""
        if VERBOSE:
            print(f"{self.name} received:".center(80, "-"))
            print(f"{msg}".center(80))

        src, signal = itemgetter("src", "signal")(msg)

        if src not in self.inputs:
            # they initially default to remembering a low pulse for each input.
            self.inputs[src] = "LOW"

        self.inputs[src] = signal

        bundle = []
        if self.all_high:
            # if it remembers high pulses for all inputs, it sends a low pulse;
            out_signal = LOW
        else:
            # otherwise, it sends a high pulse.
            out_signal = HIGH

        for target in self.targets:
            self.pulses[out_signal] += 1
            new_msg = {"src": self.name, "signal": out_signal, "tgt": target}
            bundle.append(new_msg)

        if VERBOSE:
            print(f"returning: {bundle}".center(80))
        return bundle


class Broadcaster(Node):
    """Doc String"""

    def __init__(self, name: str, targets: list) -> None:
        self.name = name
        self.targets = targets

    def __str__(self) -> str:
        return f"BC ({self.name}): -> {', '.join(self.targets)} "

    def process(self, msg: dict) -> list:
        """There is a single broadcast module (named broadcaster).
        When it receives a pulse, it sends the same pulse to all
        of its destination modules."""
        if VERBOSE:
            print(f"{self.name} received:".center(80, "-"))
            print(f"{msg}".center(80))
        _, signal, _ = itemgetter("src", "signal", "tgt")(msg)

        bundle = []
        for target in self.targets:
            self.pulses[signal] += 1
            new_msg = {
                "src": self.name,
                "signal": signal,
                "tgt": target,
            }
            bundle.append(new_msg)
        if VERBOSE:
            print(f"returning: {bundle}".center(80))

        return bundle


def parse_input(source: str = "input.txt") -> dict:
    """For parsing source string into usable content"""
    if source.endswith(".txt"):
        source = open(source).read()

    raw = source.split("\n")

    circuits = {}

    for row in raw:
        cct, targets = row.split(" -> ")

        if cct.startswith("%"):  # build a flipflop node
            circuits[cct[1:]] = FlipFlop(cct[1:], targets.split(", "))
        elif cct.startswith("&"):  # build a Conjunction node
            circuits[cct[1:]] = Conjunction(cct[1:], targets.split(", "))
        elif cct.startswith("^"):  # special output node
            circuits[cct[1:]] = OutPut(cct[1:], [None])
        else:  # build a broadcaster node
            circuits["broadcaster"] = Broadcaster(
                "broadcaster", targets=targets.split(", ")
            )

    return circuits


###############################################################################
# SOLVE PART A ################################################################
###############################################################################


def bus_report(bus_list):
    print("Bus Report".center(80, "-"))
    for line in bus_list:
        print(str(line).center(80))


def cct_report(cct_dict: dict):
    print("CCT Report".center(80, "-"))

    for key, cct in cct_dict.items():
        print("CCT key", key.ljust(15), cct)


def node_report():
    print("Node Report".center(80, "-"))
    for key, val in Node.pulses.items():
        hl = "LOW"
        if key is HIGH:
            hl = "HIGH"

        print(f"Total {hl} pulses: {val}")


VERBOSE = False


def solve_a(data):
    """For solving PART a of day 20's puzzle."""
    circuit_dict = parse_input(data)

    pulse_bus = []

    btn = Node()
    os.system("cls")
    for _ in range(1000):
        pulse_bus.extend(btn.push())
        node_report()
        while len(pulse_bus) > 0:
            if VERBOSE:
                cct_report(circuit_dict)
                bus_report(pulse_bus)

            line = pulse_bus.pop(0)
            if VERBOSE:
                print(
                    "\n",
                    "POPPED:".center(80, "-"),
                    "\n",
                    f"{line}".center(80),
                )

            tgt_node = circuit_dict[line["tgt"]]

            pulse_bus.extend(tgt_node.process(line))

            # _ = input()

    solution = math.prod(Node.pulses.values())
    return solution


###############################################################################
# MAIN ENTRY POINT FOR SUBMITTING AND BENCHMARKING ############################
###############################################################################


def main(source):
    """Main entry point"""
    return solve_a(source)


###############################################################################
# RUNNING_FROM_HOME ###########################################################
###############################################################################

if __name__ == "__main__":
    os.system("cls")
    __run_on_example__ = 2

    if __run_on_example__ == 1:
        my_utilities.version_increment(__file__, sml=1)
        answer = solve_a("example1.txt")
        print(f"My answer [{answer}] matches example: {answer == __example_answer_1__}")

    elif __run_on_example__ == 2:
        my_utilities.version_increment(__file__, sml=1)
        answer = solve_a("example2.txt")
        print(f"My answer [{answer}] matches example: {answer == __example_answer_2__}")

    else:
        my_utilities.version_increment(__file__, med=1)
        answer = main("input.txt")
        my_utilities.check_answer_a(YEAR, DAY, answer)
