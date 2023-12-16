"""usage:
to test against examples:
    reporting.py -y 2023 -d 8 -e "6,6"
to submit to aocd:
    reporting.py -y 2023 -d 8

"""
import os
import sys
from configparser import ConfigParser
from datetime import datetime
import aocd

arg_keys = sys.argv[1:]
arg_dict = {x.lower(): y for x, y in zip(arg_keys[0::2], sys.argv[1::2])}

if "-y" in arg_dict:
    year = int(arg_dict["-y"])
else:
    year = datetime.now().year

if "-d" in arg_dict:
    day = int(arg_dict["-d"])
else:
    day = datetime.now().day

if "-e" in arg_dict:
    EXAMPLE = True
    correct_example_a, correct_example_b = arg_dict["-e"].split(",")
else:
    EXAMPLE = False
    correct_example_a, correct_example_b = None, None


class TestMySolve:
    """tester for AoC puzzle solutions"""
    def __init__(
        self,
        thisyear: int,
        thisday: int,
        EXAMPLE: bool,
        correct_example_a=None,
        correct_example_b=None,
    ):
    """ Placeholder Doc String """
        self.file_to_test = ""
        self.thisyear = thisyear
        self.thisday = thisday
        self.padded_day = str(self.thisday).rjust(2, "0")
        self.EXAMPLE = EXAMPLE
        self.correct_example_a = correct_example_a
        self.correct_example_b = correct_example_b
        self._me = aocd.models.User(token=self.cfg.get(section="friargregarious", option="token")) 
        self._puzzle = aocd.models.Puzzle(self.thisyear, self.thisday, user=self._me)

    @property
    def root(self):
        return os.getcwd().replace("\\", "/")

    @property
    def solve_file_loc(self):
        
        return self.root + f"AOC {self.thisyear}/Day {self.padded_day}/"

    @property
    def solve_file(self):
        return self.solve_file_loc + f"Solve_{thisyear}_{self.padded_day}.py"



    @property
    def set_cfg(self, file_name):
        self.cfg = ConfigParser()
        # cfg.read(f"{root}/my_utilities/.env")
        self.cfg.read(".env")

    def puzzle(self):
        token = self.
        self.me = 
        

        report_msg = "\n".join(test_report)
        os.system("cls")
        print(report_msg)

        for row in [("A", final_answer_a), ("B", final_answer_b)]:
            part, my_answer = row
            print(f"Your answer for REAL Part [{part}]: {my_answer} is: ")

            if part == "A" and not this_puzzle.answered_a:
                this_puzzle.answer_a = my_answer

            if part == "B" and this_puzzle.answered_a and (not this_puzzle.answered_b):
                this_puzzle.answer_b = my_answer




def test_puzzle_report(
    thisyear: int,
    thisday: int,
    EXAMPLE: bool,
    correct_example_a=None,
    correct_example_b=None,
):
    """example/answers"""

    test_report = ["TEST REPORT".center(80, "-")]
    os.system("cls")

    if EXAMPLE:
        data_file = "example.txt"
    else:
        data_file = "input.txt"

    test_report.append("Running test on:".ljust(40, ".") + data_file.rjust(40, "."))
    data = open(data_file, encoding="utf-8").read()
    final_answer_a, final_answer_b = main(data)

    if EXAMPLE:
        for row in [
            ("A", correct_example_a, final_answer_a),
            ("B", correct_example_b, final_answer_b),
        ]:
            part, c_answer, my_answer = row
            is_good = my_answer == c_answer

            msg = f"Your answer for EXAMPLE Part [{part}]: {my_answer} is "

            if is_good:
                msg += "CORRECT!!"
                CLR = "green"

            if not is_good:
                msg += f"NOT CORRECT!!\nThe correct answer is {c_answer}"
                CLR = "red"

            test_report.append(colored(msg, color=CLR))

            report_msg = "\n".join(test_report)
            os.system("cls")
            print(report_msg)

    else:
