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

    def possible_msg(self, limits):
        """Doc placeholder"""
        self._limits = limits
        if self.is_possible:
            return colored("This game was Possible", "black", "on_yellow")
        return colored("This game was NOT Possible", "white", "on_red")

    def __repr__(self):
        """Doc placeholder"""
        return self.report()

    def power(self):
        """Used in part B equation"""
        guesses = []
        for res in self.results.items():
            guesses.append(max(res))
            guess = math.prod(guesses)
        print(f"The product of {[f'{x}' for x in guesses ]} is {guess}")

    def report(self, limits=False):
        """Doc placeholder"""
        msg = f"{self.game_name}"
        if limits is not False:
            pos_msg = self.possible_msg(limits)
            spacer = " " * (50 - len(pos_msg))
            msg += spacer + pos_msg + "\n"
        else:
            msg += "\n"

        for key, val in self.results.items():
            # print("raw", key, val)
            msg += f"{key}: {max(val)} vs ".rjust(15)

            if limits:
                msg += f"{limits[key]} LIMIT".rjust(10) + "\n"
            else:
                msg += "\n"

        return msg


class WorkSet:
    """Doc placeholder"""

    def __init__(self, limit, data_list):
        """Doc placeholder"""
        self.limits = limit
        self.games = {}

        for row in data_list:
            x = build_game(row)
            self.games[x.game_id] = x

    def report(self, with_limits=False):
        """Doc placeholder"""

        rep = []
        for _, game in self.games.items():
            rep.append(game.report(with_limits))
        return rep

    def game_is_possible(self, game_data):
        """Doc placeholder"""
        return all([self.limits[k] >= max(v) for k, v in game_data.results.items()])

    @property
    def get_answer(self):
        """Doc placeholder"""
        total = 0
        for k, val in self.games.items():
            if self.game_is_possible(val):
                total += k
        return f"The sum of possible games is {total}"


os.system("cls")
raw = open("example.txt").read().split("\n")
data = [x for x in raw if not x.isspace()]

limits = {"red": 12, "blue": 14, "green": 13}
results = {}


my_workset = WorkSet(limit=limits, data_list=data)

print("".join(my_workset.report(my_workset.limits)))

for g_ame in my_workset.games.values():
    g_ame.power()

# print(my_workset.get_answer)
# mygame = build_game("Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue")
# mygame.set_limits(limits)
# print(mygame.report(limits=True))
