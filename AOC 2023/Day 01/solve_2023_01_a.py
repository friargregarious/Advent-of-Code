"""I'm on day 18 but I had to go back and redo this to help a buddy"""
# import json
import os

numwords = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def parsed(data):
    def portion_a(words):
        foundA = {}
        for word in words:
            if len(word) > 0:
                foundA[word] = {}

                parts_found = {}
                for i, char in enumerate(word):
                    if char.isdigit():
                        parts_found[i] = int(char)
                foundA[word] = parts_found
        return foundA

    def portion_b(words):
        foundB = {}
        for word in words:
            if len(word) > 0:
                parts_found = {}
                for num_word, value in numwords.items():
                    how_many = word.count(num_word)
                    pointer = 0
                    for _ in range(how_many):
                        nw_index = word[pointer:].find(num_word)
                        parts_found[nw_index] = value
                        pointer = nw_index + 1
                foundB[word] = parts_found
        return foundB

    if __run_on_example__:
        data = open("exampleA.txt").read().split("\n")
        part_a_parsed = portion_a(data)

        # for part b, it's a different list of words,
        # but both portions need to contribute
        data = open("exampleB.txt").read().split("\n")
        temp_a = portion_a(data)
        temp_b = portion_b(data)

        part_b_parsed = {key: dict(sorted(list(temp_a[key].items()) + list(temp_b[key].items()))) for key in temp_a}

    else:
        part_a_parsed = portion_a(data.split("\n"))
        part_b_parsed = portion_b(data.split("\n"))

    return foundA, foundB


def solve_a(data):
    #  Answer Part A
    print("********* Part A")

    all_vals = []
    for key, val in data.items():
        digit_str = ""
        if len(val) == 0:
            # print(key, "no numbers, outputting '0'.")
            digit_str = "00"
        else:
            digits_list = list(dict(sorted(val.items())).values())

            digit_str = str(digits_list[0]) + str(digits_list[-1])
            # print(key, digit_str)

        all_vals.append(int(digit_str))
    print(sum(all_vals))
    return sum(all_vals)


def solve_b(a_found, b_found):
    print("********* Part B")
    all_found = {}
    for key in a_found:
        all_digits = {}
        all_digits.update(a_found[key])
        all_digits.update(b_found[key])
        all_found[key] = dict(sorted(all_digits.items()))

    all_vals = []
    for key, val in all_found.items():
        digit_str = ""
        if len(val) == 0:
            # print(key, "no numbers, outputting '0'.")
            digit_str = "00"
        else:
            digits_list = list(val.values())

            digit_str = str(digits_list[0]) + str(digits_list[-1])
            # print(key, digit_str)

        all_vals.append(int(digit_str))

    print(sum(all_vals))
    return (sum(all_vals),)


def main(source):
    if source.endswith(".txt"):
        source = open(source).read()

    found_digits_A, found_digits_B = parsed(source)

    answer_a = solve_a(found_digits_A)
    answer_b = solve_b(found_digits_A, found_digits_B)

    return (answer_a, answer_b)


__run_on_example__ = False
if __name__ == "__main__":
    os.system("cls")
    __run_on_example__ = True

    main("input.txt")
    # main("example.txt")
