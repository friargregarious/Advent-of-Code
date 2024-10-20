""" new attempt to get it right """
import os
import json
from num2words import num2words as n2w

os.system("cls")

data = open("input.txt", encoding="UTF-8").read().split("\n")
# data = open("example.txt", encoding="UTF-8").read().split("\n")

class CalibrationValue:
    """class doc placeholder"""

    nums = [(str(x), n2w(x)) for x in range(10)]

    def __init__(self, original):
        """method doc placeholder"""
        self.original = original
        assert len(self.original) > 0

    def digit_str(self, part="A"):
        """method doc placeholder"""
        result = ""
        if part == "A":
            sort_key = sorted(self.ints_indexes.keys())
            for key in sort_key:
                result += self.ints_indexes[key]
        else:
            sort_key = sorted(self.all_numbers.keys())
            for key in sort_key:
                result += self.all_numbers[key]
        return result

    @property
    def all_numbers(self):
        """method doc placeholder"""
        temp = self.ints_indexes
        temp.update(self.words_indexes)
        return temp

    def value(self, part="A"):
        """returns only the first and last digit in a digits_str"""
        # s = int(digits_str[0] + digits_str[-1])
        # report[i][part]["relevant"] = s
        # return int(self.all_numbers[0] + self.all_numbers[-1])
        return int(self.digit_str(part)[0] + self.digit_str(part)[-1])

    @property
    def total_ints(self):
        """method doc placeholder"""
        counts = [self.original.count(x[0]) for x in self.nums]
        return sum(counts)

    @property
    def total_words(self):
        """method doc placeholder"""
        counts = [self.original.count(x[1]) for x in self.nums]
        return sum(counts)

    @property
    def ints_indexes(self):
        """method doc placeholder"""
        found = {}
        for i, char in enumerate(self.original):
            if char.isnumeric():
                found[i] = char
        return found

    @property
    def words_indexes(self):
        """method doc placeholder"""
        found = {}
        for num_int, num_word in self.nums:
            how_many = self.original.count(num_word)
            pointer = 0
            position = 0
            for _ in range(how_many):
                position = self.original[pointer:].find(num_word)
                found[pointer + position] = num_int
                pointer = position + 1
        return found


# PART A #################################################
# total = 0
all_words = [CalibrationValue(line) for line in data]
for word in all_words:
    # print(word.original, word.ints_indexes)
    print(
        word.value(),
        word.digit_str().rjust(8),
        "---",
        word.value("B"),
        word.digit_str("B").ljust(8),
        word.original,
    )

print(f"Total Part A: {sum([word.value() for word in all_words])}")
print(f"Total Part B: {sum([word.value('B') for word in all_words])}")

# PART B #################################################
# first, we find all the words that are numbers
