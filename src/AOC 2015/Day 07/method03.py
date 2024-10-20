import os
from datetime import datetime

os.system("cls")

msg = "Would you like to run on the example data? \n> "
with_examples = "Y" == str(input(msg)).upper()
msg = "How many bits in each binary? \n> "
BITS = int(input(msg) or "16")


def build_data(test_data=False):
    """Method Doc Placeholder"""

    if test_data:
        data = open("example.txt", encoding="UTF-8")
    else:
        data = open("input.txt", encoding="UTF-8")

    raw_lines = enumerate(data.readlines())
    return {id: item for id, item in raw_lines}


def is_bin(test_str):
    """tests for binary condition"""
    is_str = isinstance(test_str, str)
    bin_test = len(test_str) == BITS and test_str.isnumeric()

    int_test = not test_str.isnumeric()
    add_test = not len(test_str) < BITS and test_str.isalpha()
    return all([is_str, int_test, add_test, bin_test])


def is_int(test_str):
    """tests for integer condition"""
    is_str = isinstance(test_str, str)
    int_test = test_str.isnumeric()

    add_test = not len(test_str) < BITS and test_str.isalpha()
    bin_test = not len(test_str) == BITS and test_str.isnumeric()
    return all([is_str, int_test, add_test, bin_test])


def is_add(test_str):
    """tests for address condition"""
    is_str = isinstance(test_str, str)
    add_test = len(test_str) < BITS and test_str.isalpha()

    int_test = not test_str.isnumeric()
    bin_test = not len(test_str) == BITS and test_str.isnumeric()
    return all([is_str, int_test, add_test, bin_test])


def BIN(n):
    """n = int()
    convert decimal n to bit sized binary string
    """
    if is_int(n):
        return bin(n).replace("0b", "").rjust(self.bits, "0")
    return TypeError


class LineItem:
    """Contains the information for each line that is computed"""

    def __init__(self, original):
        self.original = original.strip("\n")
        self.values = {}

    @property
    def sources(self):
        """Method Doc Placeholder"""

        if self.c_type in ["AND", "OR"]:
            a, _, c, _, _ = self.original.split()
            return [a, c]

        if self.c_type in ["NOT"]:
            _, b, _, _ = self.original.split()
            return [b]

        # if self.c_type in ["LSHIFT", "RSHIFT"]:
        return [self.original.split()[0]]

    @property
    def c_type(self):
        """Method Doc Placeholder"""
        # instructions = ["AND", "OR", "NOT", "LSHIFT", "RSHIFT"]
        # for inst_type in instructions:
        for inst_type in ["AND", "OR", "NOT", "LSHIFT", "RSHIFT"]:
            if inst_type in self.original:
                return inst_type
        return "PUT"

    @property
    def target(self):
        """Method Doc Placeholder"""
        return self.original.split()[-1]

    @property
    def addresses(self):
        """Method Doc Placeholder"""
        addresses = [self.target]
        for part in self.sources:
            if part.isalpha():
                addresses.append(part)

        return addresses
        # return [self.target].extend(self.sources)

    @property
    def completed(self):
        """Method Doc Placeholder"""
        multi = all(self.multi["values"])
        singl = self.single["value"]
        return multi or singl

# for inst_id in build_data(with_examples)

instruction_set = {id: LineItem(line) for id, line in build_data(with_examples).items()}
address_book = {}
for str_id, item in instruction_set.items():
    # print(
    #     str(str_id).rjust(3),
    #     "Original:",
    #     item.original.ljust(20),
    #     "Type:",
    #     item.c_type.ljust(7),
    #     "Target:",
    #     item.target.rjust(2),
    #     "Sources",
    #     str(item.sources).ljust(14),
    #     "Addresses",
    #     item.addresses,
    # )

    # address_book[str_id] = {
    #     "target": item.target,
    #     "sources": {a: "" for a in item.sources},
    # }
    for x in item.sources:
        if is_add(x) and 
            

