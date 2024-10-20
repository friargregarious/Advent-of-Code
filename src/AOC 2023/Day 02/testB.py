""" Doc placeholder """
import os
import math
from termcolor import colored


def build_game(line_data):
    """Doc placeholder"""
    x = Game(line_data)

    results = {"red": [], "green": [], "blue": []}

    game_data = line_data.split(": ")[1]
    # print("game_data", game_data)
    for rounds in game_data.split("; "):
        # print("rounds", rounds)
        for colour in rounds.split(", "):
            # print("colour", colour)
            qty, clr = colour.split(" ")
            # print(f"QTY: {qty} {clr}")
            results[clr].append(int(qty))
    x.results = results
    # print("RESULTS:", x.RESULTS)

    return x


class Game:
    """Doc placeholder"""

    def __init__(self, line):
        """Doc placeholder"""
        self.original = line
        self.game_name = self.original.split(": ")[0]
        self.game_id = int(self.game_name.split(" ")[1])
        self.results = {}
        self._limits = {}

    @property
    def is_possible(self):
        """Doc placeholder"""
        return all([self._limits[k] >= max(v) for k, v in self.results.items()])

    def power(self):
        """Used in part B equation"""
        guesses = []
        for res in self.results.values():
            guesses.append(max(res))
        guess = math.prod(guesses)

        msg = f"{guess} is the product of "
        msg += f"{[f'{x}' for x in guesses ]} in"
        msg += f" {self.game_name}.\n"
        msg += "".join([str(x) for x in self.results.values()])

        return guess, msg + "\n"


class WorkSet:
    """Doc placeholder"""

    def __init__(self, limit, data_list):
        """Doc placeholder"""
        self.limits = limit
        self.games = {}

        for row in data_list:
            if row != "\n":
                x = build_game(row)
                self.games[x.game_id] = x

    @property
    def solve_A(self):
        """Doc placeholder"""
        total = 0
        for k, val in self.games.items():
            if self.game_is_possible(val):
                total += k
        return f"The sum of possible games is {total}"


os.system("cls")
data = open("input.txt").read().split("\n")
#  = [x for x in raw if not x.isspace()]

limits = {"red": 12, "blue": 14, "green": 13}

my_workset = WorkSet(limit=limits, data_list=data)
total = 0
for g_ame in my_workset.games.values():
    val, msg = g_ame.power()
    print(msg)
    print(f"Running Total: {total+val} = [{total}+{val}]")
    print("*"*50)
    total += val

# print(my_workset.get_answer)
# mygame = build_game("Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue")
# mygame.set_limits(limits)
# print(mygame.report(limits=True))
