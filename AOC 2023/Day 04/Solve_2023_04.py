"""
#
#                              ADVENT OF CODE: 2023
#                                  Scratchcards
#                      https://adventofcode.com/2023/day/4
#
###############################################################################
#
# SOLVER:   friargregarious (greg.denyes@gmail.com)
# SOLVED:   {#SOLVED}
# HOME:     https://github.com/friargregarious
# SOURCE:   https://github.com/friargregarious/AOC-2023
#
# WRITTEN AND TESTED IN PYTHON VER 3.11.6
"""

###############################################################################
# IMPORTS #####################################################################
###############################################################################
import os
from configparser import ConfigParser
import aocd
# import math


data = open("input.txt", encoding="UTF-8").read()
# data = open("example.txt", encoding="UTF-8").read()
###############################################################################
# {example 1}


def build_card(card_str):
    c = ScratchCardA()
    wstart = card_str.find(":")
    csm = card_str.find("|")

    c.card_name = int(card_str.split(":")[0].replace("Card ", ""))
    c.winners = [
        int(x) for x in card_str[wstart + 1 : csm].strip(" ").split(" ") if len(x) > 0
    ]
    c.scratched = [
        int(x) for x in card_str[csm + 1 :].strip(" ").split(" ") if len(x) > 0
    ]
    return c


class ScratchCardA(list):
    """placeholder statement"""

    def __init__(self):  # , original
        # Card  10: 82 35 83 64 60 84 67 62 24 77 | 93 32  7 12 84 24 94 43 65 44 17 45 38 62 80 95 77 26 73 28 91 57 60 55  4
        # winning, mine = numbers.split(" | ")
        self.card_name: int
        self.winners: list  # = [int(x) for x in winning.split(" ")]
        self.scratched: list  # = [int(x) for x in mine.split(" ")]

    @property
    def same_numbers(self):
        """placeholder statement"""
        return [value for value in self.winners if value in self.scratched]

    @property
    def card_value(self):
        """placeholder statement"""
        v = 2 ** (len(self.same_numbers) - 1)

        if len(self.same_numbers) == 1:
            return 1

        if v < 1:
            return 0

        return v


def solve_a(source):
    """placeholder statement"""

    # In the above example, card 1 has five winning numbers (41, 48, 83, 86, and 17) and eight numbers you have (83, 86, 6, 31, 17, 9, 48, and 53). Of the numbers you have, four of them (48, 83, 17, and 86) are winning numbers! That means card 1 is worth 8 points (1 for the first match, then doubled three times for each of the three matches after the first).

    # Card 2 has two winning numbers (32 and 61), so it is worth 2 points.
    # Card 3 has two winning numbers (1 and 21), so it is worth 2 points.
    # Card 4 has one winning number (84), so it is worth 1 point.
    # Card 5 has no winning numbers, so it is worth no points.
    # Card 6 has no winning numbers, so it is worth no points.
    # So, in this example, the Elf's pile of scratchcards is worth 13 points.

    cards = [build_card(x) for x in source.split("\n") if len(x) > 1]
    points = [card.card_value for card in cards]
    print([card.same_numbers for card in cards])
    print(points)
    print(sum(points))

    return sum(points)


###############################################################################
# {example 2}


def solve_b(source):
    """placeholder statement"""

    cards = {i + 1: build_card(x) for i, x in enumerate(source.split("\n"))}

    how_many = {card.card_name: 1 for card in cards.values()}

    # for index, card in cards.items():
    #     print(index, card.card_name, card.same_numbers)

    for index, card_count in how_many.items():
        new_cards = [
            index + 1 + x for x in range(len(cards[index].same_numbers))
        ] * card_count
        msg = f"Card #{cards[index].card_name}" + "\t"
        msg += f"has {len(cards[index].same_numbers)} wins" + "\t"
        msg += f"and produces new cards: {new_cards}"
        # print(msg)
        for bonus_card in new_cards:
            how_many[bonus_card] += 1

    answer = sum(how_many.values())
    print(f"The total sum of cards scratched: {answer}")

    return answer


###############################################################################
# ENTRY POINT FOR SUBMITTING & BENCHMARKING


def main(source):
    """placeholder statement"""
    return (solve_a(source=source), solve_b(source=source))


if __name__ == "__main__":
    os.system("cls")
    # data = open("example.txt", encoding="utf-8").read()
    data = open("input.txt", encoding="utf-8").read()
    final_answer_a, final_answer_b = main(data)
    # main()

    cfg = ConfigParser()
    cfg.read("C:/Advent of Code/.env")
    token = cfg.get(section="friargregarious", option="token")
    me = aocd.models.User(token=token)
    this_puzzle = aocd.models.Puzzle(year=2023, day=4, user=me)

    if not this_puzzle.answered_a:
        this_puzzle.answer_a = final_answer_a
    if not this_puzzle.answered_b:
        this_puzzle.answer_b = final_answer_b
