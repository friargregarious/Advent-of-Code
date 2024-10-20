###############################################################################
#
#                              ADVENT OF CODE: 2023
#                                  Camel Cards
#                      https://adventofcode.com/2023/day/7
#
###############################################################################
#
# SOLVER:   friargregarious (greg.denyes@gmail.com)
# SOLVED:   {#SOLVED}
# HOME:     https://github.com/friargregarious
# SOURCE:   https://github.com/friargregarious/AOC-2023
#
# WRITTEN AND TESTED IN PYTHON VER 3.11.6
#
###############################################################################
# IMPORTS #####################################################################
###############################################################################

import os
from configparser import ConfigParser
from termcolor import colored
import aocd

# import math

###############################################################################
# GATHER TOOLS ################################################################
###############################################################################


def parse_input(source):
    """let's make this readable"""
    raw = source.split("\n")
    return [(row[:5], int(row[6:])) for row in raw if len(row) > 1]


def card_strength(card):
    """PART A VERSION"""
    card_list = "AKQJT98765432"
    return len(card_list) - card_list.index(card)


def b_card_strength(card):
    """PART B VERSION"""
    card_list = "AKQT98765432J"
    return len(card_list) - card_list.index(card)


def hand_builder(hand, bid, part_ref):
    """for building hand objects for either part a or b"""
    h = CardHand(hand=hand, bid=bid)
    if part_ref == "A":
        h.card_strength = card_strength
        # h.hand_scoring = hand_scoring
    if part_ref == "B":
        h.card_strength = b_card_strength
        h.wild = "J"

    return h


class CardHand:
    """Docs place holder"""

    def __init__(self, hand, bid):
        self.wild = False
        self.hand = hand
        self.bid = bid

    def card_strength(self, card):
        """placeholder for Part A/B versions"""
        return -1

    @property
    def hand_scoring(self):
        """ranks based on which part we are doing"""

        cnt_j = self.hand.upper().count("J")
        hand_nj = self.hand.replace("J", "")

        iter_hand = list(self.hand)
        distinct = set(iter_hand)
        c_cnt = [self.hand.count(a) for a in distinct]

        crd_str_order = [self.card_strength(x) for x in iter_hand]

        iter_hand_nj = list(hand_nj)
        distinct_nj = set(iter_hand_nj)
        c_cnt_nj = [hand_nj.count(a) for a in distinct]

        def one_of_kind(hand):
            """High card          0"""
            # A: A2345
            # B: A2345
            return len(distinct) == 5 and cnt_j == 0

        def one_pair(hand):
            """TWO OF A KIND (ONE PAIR)          10"""
            return (self.wild and (2 == max(c_cnt_nj) + cnt_j)) or (
                not self.wild and max(c_cnt) == 2
            )
            # A: AA234
            # B: AJ234

        def three_of_kind(hand):
            """THREE OF A KIND   30"""
            # A: 23AAA
            # B: 23AAJ, 23AJJ
            return (self.wild and len(c_cnt_nj) == 3 == max(c_cnt_nj) + cnt_j) or (
                not self.wild and len(c_cnt) == 3 == max(c_cnt)
            )

        def four_of_kind(hand):
            """# FOUR OF A KIND    50"""
            # A: 8AAAA
            # B: 8AAAJ, 8AAJJ, 8AJJJ

            return (self.wild and 4 == max(c_cnt_nj) + cnt_j or max(c_cnt) == 4) or (
                not self.wild and max(c_cnt) == 4
            )

        def five_of_kind(hand):
            # FIVE OF A KIND    60
            # A: AAAAA
            # B: AAAAA, JJJJJ, AJJJJ, AAJJJ, AAAJJ, AAAAJ

            return (self.wild and max(c_cnt) + cnt_j == 5)(
                not self.wild and len(c_cnt) == 1 and max(c_cnt) == 5
            )

        def two_pairs(hand):
            # 2 PAIRS          20
            # A: AA244
            # B: AA29J X, AA2JJ X, AA99J X

            return (self.wild and c_cnt.count(2) == 2) or (
                not self.wild and c_cnt.count(2) == 2
            )

        def full_house(hand):
            # FULL HOUSE: THREE OF ONE + TWO OF ONE:         40
            # A: 22333
            # B: 2233J
            return (self.wild and len(distinct_nj) == 2 and cnt_j == 1) or (
                len(distinct) == 2 and (max(c_cnt) == 3) and (min(c_cnt) == 2)
            )

            if five_of_kind(self.hand):
                """FIVE OF A KIND    60"""
                return [60] + crd_str_order

            if four_of_kind(self.hand):
                """# FOUR OF A KIND    50"""
                return [50] + crd_str_order

            if full_house(self.hand):
                return [40] + crd_str_order

            if three_of_kind(self.hand):
                """THREE OF A KIND   30"""
                return [30] + crd_str_order

            if two_pairs(self.hand):
                """2 PAIRS          20"""
                return [20] + crd_str_order

            if two_of_kind(self.hand):
                """TWO OF A KIND (ONE PAIR)     10"""
                return [10] + crd_str_order

            if high_card(self.hand):
                return [0] + crd_str_order


###############################################################################
# PART A ######################################################################
###############################################################################


def solve_a(source):
    # So, the first step is to put the hands in order of strength:
    scored_hands = []
    all_hands = []

    for hand, bid in parse_input(source):
        all_hands.append(hand_builder(hand, bid, "A"))

    for hand in all_hands:
        scored_hands.append(hand.hand_scoring + [hand.hand, hand.bid])

    scored_hands.sort()

    # Now, you can determine the total winnings of this set of hands
    # by adding up the result of multiplying each hand's bid with
    # its rank (765 * 1 + 220 * 2 + 28 * 3 + 684 * 4 + 483 * 5).
    # So the total winnings in this example are 6440.

    winnings = []
    rep = ["## A #############################"]
    print(f"Part A has {len(scored_hands)} hands ready to rank.")
    for index, row in enumerate(scored_hands):
        ranking = index + 1
        hand_wins = row[-1] * ranking

        msg = str(row).ljust(40)
        msg += f"{row[-1]:,}".rjust(13) + " * "
        msg += f"{ranking}".rjust(4) + " = "
        msg += f"{hand_wins:,}".rjust(8)

        winnings.append(hand_wins)

        rep.append(msg)

    solution = sum(winnings)

    rep.append("Final Tally:" + f"{solution:,}".rjust(15))
    a_rep = "\n".join(rep)
    open("a_test_output.txt", "w", encoding="utf_8").write(a_rep)

    return solution


###############################################################################
# PART B ######################################################################
###############################################################################


def solve_b(source):
    """now we mess with Jokers"""
    # So, the first step is to put the hands in order of strength:
    scored_hands = []
    all_hands = []

    for hand, bid in parse_input(source):
        all_hands.append(hand_builder(hand, bid, "B"))

    for hand in all_hands:
        scored_hands.append(hand.hand_scoring + [hand.hand, hand.bid])

    scored_hands.sort()

    # Now, you can determine the total winnings of this set of hands
    # by adding up the result of multiplying each hand's bid with
    # its rank (765 * 1 + 220 * 2 + 28 * 3 + 684 * 4 + 483 * 5).
    # So the total winnings in this example are 6440.

    winnings = []
    rep = ["## B #############################"]
    for index, row in enumerate(scored_hands):
        ranking = index + 1
        hand_wins = row[-1] * ranking

        msg = str(row).ljust(40)
        msg += f"{row[-1]:,}".rjust(13) + " * "
        msg += f"{ranking}".rjust(4) + " = "
        msg += f"{hand_wins:,}".rjust(8)

        winnings.append(hand_wins)
        rep.append(msg)
    solution = sum(winnings)

    rep.append("Final Tally:" + f"{solution:,}".rjust(15))
    b_rep = "\n".join(rep)
    open("b_test_output.txt", "w", encoding="utf_8").write(b_rep)

    return solution


###############################################################################
# MAIN ENTRY POINT FOR SUBMITTING & BENCHMARKING ##############################
###############################################################################


def main(source):
    return (solve_a(source=source), solve_b(source=source))


###############################################################################
# RUNNING FROM HOME ###########################################################
###############################################################################
if __name__ == "__main__":
    THISYEAR, THISDAY = 2023, 8
    # set the example flag here
    EXAMPLE = False
    # EXAMPLE = True
    C_ANS_A = 6
    C_ANS_B = 6

    os.system("cls")

    if EXAMPLE:
        data = open("example2.txt", encoding="utf-8").read()
    else:
        data = open("input.txt", encoding="utf-8").read()

    final_answer_a, final_answer_b = main(data)

    if EXAMPLE:
        for row in [("A", 6, final_answer_a), ("B", 6, final_answer_b)]:
            part, c_answer, my_answer = row
            is_good = my_answer == c_answer

            if is_good:
                msg = f"Your answer for {part}: {my_answer} is CORRECT!!"
                CLR = "green"

            if not is_good:
                msg = f"Your answer for {part}: {my_answer} is NOT CORRECT!!\n"
                msg += f"The correct answer is {c_answer}"
                CLR = "red"

            print(colored(msg, color=CLR))

    else:
        cfg = ConfigParser()
        cfg.read("C:/Advent of Code/.env")
        token = cfg.get(section="friargregarious", option="token")
        me = aocd.models.User(token=token)
        this_puzzle = aocd.models.Puzzle(THISYEAR, THISDAY, user=me)

        if not this_puzzle.answered_a:
            this_puzzle.answer_a = final_answer_a

        elif this_puzzle.answered_a and not this_puzzle.answered_b:
            this_puzzle.answer_b = final_answer_b
        else:
            print("You've answered these puzzles already!")
