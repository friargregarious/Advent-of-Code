import os

# from datetime import datetime

os.system("cls")

msg = "Would you like to run on the example data? \n> "
with_examples = "Y" == str(input(msg)).upper()
msg = "How many bits in each binary? \n> "
BITS = int(input(msg) or "16")


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

            if is_bin(a):
                a = bin(a)
            if is_bin(c):
                c = bin(c)

            return [a, c]

        if self.c_type in ["NOT"]:
            _, b, _, _ = self.original.split()
            if is_bin(b):
                b = bin(b)

            return [b]

        # if self.c_type in ["LSHIFT", "RSHIFT"]:
        a = self.original.split()[0]
        if is_bin(a):
            a = bin(a)

        return [a]

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
    bin_test = test_str.isnumeric() and not (len(test_str) == BITS)
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
    n = int(n)
    return bin(n).replace("0b", "").rjust(BITS, "0")


def NOT(x):
    """reverses the bits"""
    assert len(x) == 16
    assert x.isnumeric()

    answer = ""
    for char in x:
        if char == "1":
            answer += "0"
        else:
            answer += "1"

    assert len(answer) == 16
    assert answer.isnumeric()

    return answer

def get_inst(item):
    # returns the instruction from the item

def check_sources(item):
    # returns 

    # de = {'RSHIFT': ['dd']}
    # lt = {'NOT': ['ls']}
    # lj = {'OR': ['lh', 'li']}
    if isinstance(item, str):
        return "Done"

    if isinstance(item, dict):
        truths = [len(x) == BITS for x in item.values()]

        if all(truths):
            return "Ready"

        if any(truths):
            return "Some"

    return "None"

            

if __name__ == "__main__":
    instruction_set = {
        inst_id: LineItem(line) for inst_id, line in build_data(with_examples).items()
    }

    address_book = {}
    for instr, item in instruction_set.items():
        # for address in item.addresses:
        #     address_book.add(address)
        address_book[item.target] = {item.c_type: item.sources}

    # do a check on the sources
    for target, parts in address_book.items():

        if "NOT" in parts:
            if len(parts["NOT"][0]) == 16:
                address_book[target] = NOT(parts["NOT"][0])
        elif address_book[parts["NOT"][0]] 






        # do the puts
        if "PUT" in parts and parts["PUT"][0].isnumeric():
            # print("I FOUND ONE!!!", BIN(parts["sources"][0]))
            address_book[target] = BIN(parts["PUT"][0])
    print(len(address_book))
    # print(address_book)

    open("answer.txt", "w").write(
        "\n".join(f"{a} = {b}" for a, b in address_book.items())
    )
