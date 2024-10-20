""" new attempt to get it right """
import os
import json
from num2words import num2words as n2w

os.system("cls")

data = open("input.txt", encoding="UTF-8").read().split("\n")
# data = open("example.txt", encoding="UTF-8").read().split("\n")

numwords = {str(x): n2w(x).replace("-", "").lower() for x in range(10)}
report = {}


def get_digits(i, test_str, part):
    """
    returns a string of all the digits found in a string
    get_digits(str) -> str of ints
    """

    num_line = ""
    for character in test_str:
        if character.isnumeric():  # in "0123456789":
            num_line += character

    report[i][part]["digits"] = num_line
    return num_line


def first_n_last(i, digits_str, part):
    """returns only the first and last digit in a digits_str"""
    assert len(digits_str) > 0
    s = int(digits_str[0] + digits_str[-1])
    report[i][part]["relevant"] = s
    return s


# PART A #################################################
# total = 0

for index, word in enumerate(data):
    if index not in report:
        report[index] = {"A": {}, "B": {}, "word": word}

    x = get_digits(index, word, "A")
    y = first_n_last(index, x, "A")
#     total += y


# print(index, y, x.rjust(8), word)
# print("Answer:", total, f"Should be: 56465 {total == 56465}")

# PART B #################################################
# first, we find all the words that are numbers


def get_all_digits(index, word_str, part):
    """replaces words with numbers they represent,
    returns all the integers in the word"""

    found = {}
    for integer, num_word in numwords.items():
        how_many = word_str.count(num_word)
        pointer = 0
        position = 0
        print(f"there should be {how_many} x {num_word} in {word_str}")
        for _ in range(how_many):
            position = word_str[pointer:].find(num_word)
            print(position, pointer, num_word, word_str[position:])
            found[pointer + position] = integer
            pointer = position + 1

    for i, char in enumerate(word_str):
        if char.isnumeric():
            found[i] = char

    # print(index, found)
    new_str = ""

    for z in sorted(found):
        new_str += found[z]

    report[index][part]["digits"] = new_str
    return new_str


total = 0
for index, word in enumerate(data):
    # if index not in report:
    #     report[index] = {"A": {}}

    x = get_all_digits(index, word, "B")
    y = first_n_last(index, x, "B")
    # total += y
    # print(index, y, x.rjust(8), word)

a_total = 0
b_total = 0
for index in report:
    a_total += report[index]["A"]["relevant"]
    b_total += report[index]["B"]["relevant"]

print("Answer A:", a_total)
print("Answer B:", b_total)

open("test_out2.txt", "w").write(json.dumps(report, indent=3))
