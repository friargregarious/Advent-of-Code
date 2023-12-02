###############################################################################
#
"""                            ADVENT OF CODE: 2015
                             Some Assembly Required
                      https://adventofcode.com/2015/day/7
"""
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
from datetime import datetime

data = open("input.txt", encoding="UTF-8").read()


###############################################################################
# {example 1}
class WrongMissingOperator(BaseException):
    """Exception raised for errors ......

    Attributes:
        direction -- command which caused the error
        message -- explanation of the error
    """


class MissingInstructionError(BaseException):
    """Exception raised for errors ......

    Attributes:
        direction -- command which caused the error
        message -- explanation of the error
    """


example_answers = {
    "d": 72,
    "e": 507,
    "f": 492,
    "g": 114,
    "h": 65412,
    "i": 65079,
    "x": 123,
    "y": 456,
}


def BIN(n, bits):
    """convert decimal to 16 bit binary string
    ASDFSDFSFDSF
    >>> BIN(42, 8)
    '00101010'
    >>> BIN('311', 10)
    '0100110111'
    >>> BIN(500, 16)
    '0000000111110100'


    """

    if isinstance(n, str) and len(n) < bits:
        n = int(n)

    return bin(n).replace("0b", "").rjust(bits, "0")


def PUT(x, n):
    """Doesn't really do anything, just use it to test random BIN's
    >>> PUT('1010101010101010')
    '1010101010101010'
    >>> PUT('1110111011101111')
    '1010101010101010'
    >>> PUT(500)
    '0000000111110100'
    >>> PUT(42)
    '0000000000101010'
    """

    if isinstance(x, int):
        x = BIN(x, n)

    assert len(x) == n
    assert x.isnumeric()

    return x


def NOT(x):
    """reverses the bits,
    what was, is no more and what wasn't, now is
    >>> NOT('1010101010101010')
    '0101010101010101'
    >>> NOT('1110111011101111')
    '0001000100010000'
    >>> NOT('0010011001100101')
    '1101100110011010'
    >>> NOT('1101010000010010')
    '0010101111101101'
    """
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


def AND(x, y):
    """
    >>> AND("1010101010101010", "1110111011101111")
    '1010101010101010'
    >>> AND('0010011001100101', '1101010000010010')
    '0000010000000000'
    """
    assert len(x) == len(y) == 16
    assert x.isnumeric()
    assert y.isnumeric()

    answer = ""
    for a, b in zip(x, y):
        if a == b == "1":
            answer += "1"
        else:
            answer += "0"

    assert len(answer) == 16
    assert answer.isnumeric()

    return answer


def OR(x, y):
    """
    >>> OR("1010101010101010", "1110111011101111")
    '1110111011101111'
    >>> OR('0010011001100101', '1101010000010010')
    '1111011001110111'
    """
    assert len(x) == len(y) == 16
    assert x.isnumeric()
    assert y.isnumeric()

    answer = ""
    for a, b in zip(x, y):
        if a == b == "0":
            answer += "0"
        else:
            answer += "1"

    assert len(answer) == 16
    assert answer.isnumeric()

    return answer


def LEFT(x, n):
    """00010111 (decimal +23)
        ^ front char
      <- shift this way <-
        goes to th back
     =  00101110 (decimal +46)
                  ^
    >>> LEFT('0010011001100101', 3)
    '0011001100101001'
    >>> LEFT('0011001100101001', 5)
    '0110010100100110'
    >>> LEFT('0110010100100110', 9)
    '0100110011001010'

    """
    assert len(x) == 16
    assert x.isnumeric()
    assert isinstance(n, int)

    for _ in range(n):
        first, last = x[:1], x[1:]
        x = last + first

    assert not x.isspace()
    assert x.isnumeric()

    return x


def RIGHT(x, n):
    """
         00010111 (decimal +23)
          last  ^
    -> shift goes this way ->
        goes front
      =  10001011 (decimal +46)
         ^
    >>> RIGHT('0010011001100101', 3)
    '1010010011001100'
    >>> RIGHT('0011001100101001', 5)
    '0100100110011001'
    >>> RIGHT('0110010100100110', 9)
    '1001001100110010'


    """
    assert len(x) == 16
    assert x.isnumeric()
    assert isinstance(n, int)

    for _ in range(n):
        first, last = x[:-1], x[-1:]
        x = last + first

    assert not x.isspace()
    assert x.isnumeric()

    return x


class Circuit(dict):
    """Class doc string"""

    def __init__(self, bits=16):
        """There are 8 bits in a byte,
        and byte has 8 characters,
        so 16 bit is 18 characters"""
        self.clear()
        self.bits = bits
        self.history = []
        self.log_inc = 0
        self.instructions = {}
        self.done = {}

    @property
    def to_do(self):
        """so we know how much work we have left TO DO.
        >>> gen = Circuit()
        >>> gen.instructions["AND"] = [1,2,3,4,5]
        >>> gen.instructions["OR"] = [1,2,3]
        >>> gen.instructions["LEFT"] = [1,2,3,4,5,6,7,8,9]
        >>> gen.instructions["RIGHT"] = [1]
        >>> gen.to_do
        18
        """
        sums = [len(v) for v in self.instructions.values()]
        return sum(sums)


    def submit_SHIFT(self, line):
        # et RSHIFT 5 -> ew
        address, inst, count, _, target = line.split()
        count = int(count)

        def assign():
            if inst == "LSHIFT":
                self[target] = LEFT(address, count)
            else:
                self[target] = RIGHT(address, count)
            return False

        if inst not in self.instructions:
            self.instructions[inst] = {}

        if address.isnumeric():
            # this is a Decimal and although they
            # do not appear in the inputs but we're being careful
            address = BIN(address, self.bits)
            assign()

        elif address in self:
            address = self[address]
            assign()

        return inst, [address, count, target]

    def submit_PUT(self, line):
        # PUT jd -> je
        inst, address, _, target = line.split()

        if inst not in self.instructions:
            self.instructions[inst] = {}

        if address.isnumeric():
            # PUT 1 -> je
            self[target] = PUT(int(address), self.bits)
            return False
        elif address in self:
            # PUT jd -> je
            self[target] = PUT(address, self.bits)
            return False

        parts = [address, target]
        return inst, parts

    def submit_ANDOR(self, line):

    def submit_NOT(self, line):


    def submit(self, id, line):
        """method"""
        if "SHIFT" in line:
            inst, parts = self.submit_SHIFT(line)

        elif "PUT" in line:
            inst, parts = self.submit_PUT(line)



        elif "NOT" in line:
            # NOT jd -> je
            inst, address, _, target = line.split()

            if inst not in self.instructions:
                self.instructions[inst] = {}

            if address.isnumeric():
                # NOT 1 -> je
                self[target] = NOT(BIN(address, self.bits))
            elif address in self:
                # NOT jd -> je
                self[target] = NOT(address)
            else:
                parts = [address, target]
                self.instructions[inst][id] = parts

        elif ("AND" or "OR") in line:
            # he AND hp -> hr
            # 1 AND hp -> hr
            # he AND 1 -> hr
            # he OR hp -> hr
            # 1 OR hp -> hr
            # he OR 1 -> hr

            left, inst, right, _, target = line.split()
            parts = [left, right, target]

            if inst not in self.instructions:
                self.instructions[inst] = {}

            # test for decimals and assign BIN
            if left.isnumeric():
                left = BIN(int(left), self.bits)

            if right.isnumeric():
                right = BIN(int(right), self.bits)


            # test for both BINs and apply to finished...
            if left.isnumeric() and right.isnumeric():
                if inst == "AND":
                    self[target] = AND(left, right)
                else:
                    self[target] = OR(left, right)
            else:
                # ...or to INST queue
                self.instructions[inst][id] = parts

    def work(self, target_answer):
        """function"""
        total_work = int(self.to_do)

        def progress(msg):
            p = (total_work - self.to_do) / total_work
            print(f"Progress: {p:.2f}% Completed. ", msg)

        while self.to_do > 0:
            progress(self.values())
            self.work_PUTNOT()
            self.work_SHIFTS()
            self.work_ANDORS()

        donemsg = f"WORK DONE!! Target Answer '{target_answer}'"
        donemsg += f" = {self[target_answer]}"
        print(donemsg)

    def work_PUT(self):
        """method info"""
        todelete = []
        for i, parts in self.instructions["PUT"].items():
            # parts = [address, target]
            val, target = parts
            if val.isalpha() and val in self:
                self[target] = PUT(self[val], self.bits)
                self.done[i] = parts
                todelete.append(i)
            elif val.isnumeric():
                self[target] = PUT(BIN(int(val)), self.bits)

        for a in todelete:
            del self.instructions["PUT"][a]

    def work_NOT(self):
        """method info"""
        todelete = []
        for i, parts in self.instructions["NOT"].items():
            # parts = [address, target]
            val, target = parts
            if val.isnumeric():
                self[target] = self.PUT_NOT(val, "NOT")
                self.done[i] = parts
                todelete.append(i)

        for a in todelete:
            del self.instructions["NOT"][a]

    def work_SHIFTS(self):
        """method info"""
        todelete = []
        for i, parts in self.instructions["RSHIFT"].items():
            # parts = [add, int(count), target]
            add, count, target = parts

            if add in self.keys():
                # SHIFT(self, address, direction, count, target)
                self[target] = self.SHIFT(add, "RSHIFT", count)
                self.done[i] = parts
                todelete.append(i)

        for a in todelete:
            del self.instructions["RSHIFT"][a]

        todelete = []
        for i, parts in self.instructions["LSHIFT"].items():
            # parts = [add, int(count), target]
            add, count, target = parts

            if add in self.keys():
                # SHIFT(self, address, direction, count, target)
                self[target] = self.SHIFT(add, "LSHIFT", count)
                self.done[i] = parts
                todelete.append(i)

        for a in todelete:
            del self.instructions["LSHIFT"][a]

    def work_ANDORS(self):
        """method info"""
        todelete = []
        for i, parts in self.instructions["AND"].items():
            # 1 AND ds -> dt
            # parts = [left, right, target]
            left, right, target = parts
            can_left = (left in self) or left.isnumeric()
            can_right = (right in self) or right.isnumeric()

            if can_left and can_right:
                # AND_OR(self, a_key, action, b_key, target)
                self[target] = self.AND_OR(left, "AND", right)
                self.done[i] = parts
                todelete.append(i)

        for a in todelete:
            del self.instructions["AND"][a]

        todelete = []
        for i, parts in self.instructions["OR"].items():
            # parts = [left, right, target]
            left, right, target = parts
            can_left = (left in self) or left.isnumeric()
            can_right = (right in self) or right.isnumeric()

            if can_left and can_right:
                # AND_OR(self, a_key, action, b_key, target)
                self[target] = self.AND_OR(left, "OR", right)
                self.done[i] = parts
                todelete.append(i)

        for a in todelete:
            del self.instructions["OR"][a]

    def logger(self, source, msg):
        """method"""
        self.log_inc += 1
        s_inc = str(self.log_inc).rjust(4, "0")
        id = f"[{s_inc}] - {datetime.now().isoformat()}"

        self.history.append(f"{id}: {source.upper()}: {msg}")

    def report(self, r_type="s"):
        """method"""
        temp = sorted(list(self.keys()))

        print(f"total instructions: {self.to_do}".center(80))

        for x, y in self.instructions.items():
            print(x, y)

        print("Total Finished".center(80))
        for k in temp:
            if r_type == "s":
                print(f"wire {k}: {self[k]}")
            else:
                print(f"wire {k}: {int(self[k], 2)}")


def solve_a(source):
    """function"""
    solution = source
    return solution


###############################################################################
# {example 2}


def solve_b(source):
    """function"""
    solution = source
    return solution


###############################################################################
# ENTRY POINT FOR SUBMITTING & BENCHMARKING


def main(source):
    """function"""
    return (solve_a(source=source), solve_b(source=source))


def test_funcs():
    from random import randint, choice

    vals = {}

    # first we test BIN
    def rand_bin(b=16):
        my_rand = randint(10, 10000)
        my_bin = BIN(my_rand, b)
        assert int(my_bin, 2) == my_rand
        return BIN(randint(10, 10000), b)

    # let's test AND & OR
    for index in range(10):
        shift = randint(3, 10)
        vals = {}
        vals["a"] = rand_bin()  # random BIN to start with
        vals["b"] = rand_bin()  # random BIN to start with
        vals["c"] = AND(vals["a"], vals["b"])  # AND Test
        vals["d"] = OR(vals["a"], vals["b"])  # OR Test
        vals["e"] = LEFT(vals["a"], shift)  # shift a left n steps
        vals["f"] = RIGHT(vals["e"], shift)  # shift it back to how it was

        # testing AND
        for a, b, c in zip(vals[a], vals[b], vals[c]):
            print("  a: ", a)
            print("  b: ", b)
            print("AND: ", c)

            if c == "0":
                assert not b == a
            else:
                assert l == r

        for a, b, d in zip(vals[a], vals[b], vals[c]):
            print("  a: ", a)
            print("  b: ", b)
            print(" OR: ", d)

        for l, r, z in zip(a, b, d):
            if z == "0":
                assert l == r == "0"
            else:
                assert l or r == "1"

    # Now we test the SHIFTS against each other
    for x in range(10):
        z, shift = rand_bin(), randint(1, 10)

        assert b == z
        assert a != b

        print("AND", a, b, c)


if __name__ == "__main__":
    import os

    os.system("cls")

    test_funcs()

    # myC = Circuit()
    # data = enumerate(open("input.txt", encoding="UTF-8").readlines())
    # unprocessed = {str(ln).rjust(4, "0"): line for ln, line in data}

    # for i, line in unprocessed.items():
    #     if len(line.split()) == 3:
    #         unprocessed[i] = f"PUT {line}"

    # for id, inst in unprocessed.items():
    #     myC.submit(id, inst)

    # print(myC.to_do, myC.log_inc)

    # myC.work("a")
