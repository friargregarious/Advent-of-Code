import os
import sys
from termcolor import colored, cprint
import Solve_2023_01 as so


data = open("input.txt").read().split("\n")


worklist = so.WorkList()
worklist.set_words(data)

sum_a, sum_b = 0, 0
population = len(worklist)
for index, item in enumerate(worklist):
    os.system("cls")
    sum_a += item.value("A")
    sum_b += item.value("B")

    arrow_r = " --> "
    arrow_l = " <-- "

    scolw = 2 * 6
    vcolw = 10
    ccolw = 2 * 7
    acolw = 5

    col_s_left = [
        "STRING".center(scolw),
        "-" * scolw,
        f"{item.digit_str('A')}".center(scolw),
    ]

    arrowcol_l = [
        arrow_r.center(acolw),
        "-" * acolw,
        arrow_r.center(acolw),
    ]

    col_val_left = [
        "Vals".center(vcolw),
        "-" * vcolw,
        f"{item.value('A')}".center(vcolw),
    ]

    col_cent = [
        "RUNNING TOTALS".center(ccolw),
        "-" * ccolw,
        f"[{sum_a} / {sum_b}]".center(ccolw),
    ]

    col_val_right = [
        "Vals".center(vcolw),
        "-" * vcolw,
        f"{item.value('B')}".center(vcolw),
    ]

    arrowcol_r = [
        arrow_l.center(acolw),
        "-" * acolw,
        arrow_l.center(acolw),
    ]

    col_s_right = [
        "STRING".center(scolw),
        "-" * scolw,
        f"{item.digit_str('B')}".center(scolw),
    ]

    screenwide = (scolw * 2) + (vcolw * 2) + ccolw + (acolw * 2) + 20

    print("\n", "\n", "\n", "\n", f"{index+1} / {population}".center(screenwide), "\n")
    for i in range(3):
        print(
            " " * 10,
            col_s_left[i]
            + arrowcol_l[i]
            + col_val_left[i]
            + col_cent[i]
            + col_val_right[i]
            + arrowcol_r[i]
            + col_s_right[i],
        )

    word = item.original  # .center(screenwide)
    nums_digit = item.ints_indexes
    nums_words = item.words_indexes

    wrd_row, dig_row = "", ""

    for i, char in enumerate(word):
        if i in nums_digit:
            dig_row += nums_digit[i]
        else:
            dig_row += " "

        if i in nums_words:
            wrd_row += nums_words[i]
        else:
            wrd_row += " "

    def edge_case(test_str):
        ISBLANK = test_str.isspace()
        ISLEFT = test_str[0] != " "
        ISRIGHT = test_str[-1] != " "

        ISMERGED = False
        for test in [
            "oneight",
            "twone",
            "sevenine",
            "eightwo",
            "eighthree",
            "threeight",
            "fiveight",
            "nineight",
        ]:
            if test in test_str:
                ISMERGED = True

        test_list = [ISBLANK, ISLEFT, ISRIGHT, ISMERGED]

        msg = []
        if ISBLANK:
            msg.append("EMPTY DATASET")
        if ISLEFT or ISRIGHT:
            msg.append("NUMBER ON THE EDGE")
        if ISMERGED:
            msg.append("OVERLAPPING WORDS")

        msg = "<----- " + " & ".join(msg)
        if any(test_list):
            return colored(
                msg, color="black", on_color="on_light_yellow"
            )  # , attrs="bold"
        return ""

    # Available text colors:
    #     black, red, green, yellow, blue, magenta, cyan, white,
    #     light_grey, dark_grey, light_red, light_green, light_yellow, light_blue,
    #     light_magenta, light_cyan.

    # Available text highlights:
    #     on_black, on_red, on_green, on_yellow, on_blue, on_magenta, on_cyan, on_white,
    #     on_light_grey, on_dark_grey, on_light_red, on_light_green, on_light_yellow,
    #     on_light_blue, on_light_magenta, on_light_cyan.

    print("\n")
    blank_str = " " * ((screenwide - len(word)) // 2)
    print(colored(dig_row.center(screenwide), "blue"), edge_case(dig_row))
    print(word.center(screenwide))
    print(colored(wrd_row.center(screenwide), "green"), edge_case(wrd_row))

    print("\n\n\n")
    print(f"Press <ENTER> to continue... {index+1}/{population}".center(screenwide))
    _ = input()
