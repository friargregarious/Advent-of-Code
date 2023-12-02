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
import os
from datetime import datetime

os.system("cls")

msg = "Would you like to run on the example data? \n> "

with_examples = "Y" == str(input(msg)).upper()

if with_examples:
    data = open("example.txt", encoding="UTF-8")
else:
    data = open("input.txt", encoding="UTF-8")

###############################################################################
# {example 1}

example_answers = {
    "D": 72,
    "E": 507,
    "F": 492,
    "G": 114,
    "H": 65412,
    "I": 65079,
    "X": 123,
    "Y": 456,
}


class Logger(dict):
    """Method Doc Placeholder"""

    counter = 0

    def __init__(self):
        """method"""
        self.unique_addresses = {}

    def log(self, source, msg):
        """method"""
        self.counter += 1
        s_inc = str(self.counter).rjust(4, "0")
        id = f"[{s_inc}] - {datetime.now().isoformat()}"

        self[id] = f"{source.upper()}: {msg}"


class LineItem:
    """Contains the information for each line that is computed"""

    def __init__(self, target, sources, values=(False, False), count=0):
        self.sources = sources
        self.values = values
        self.target = target
        self.count = count

    @property
    def completed(self):
        """Method Doc Placeholder
        >>> c = LineItem("a", ("df", "ed"), ("0101010101", "1010101010"))
        >>> c.completed
        True
        >>> b = LineItem("a", ("df", "ed"), (False, False))
        >>> b.completed
        False
        >>> d = LineItem("a", "df", False)
        >>> d.completed
        False
        >>> e = LineItem("a", "df", ("0101010101", False), 4)
        >>> e.completed
        False

        """
        multi = isinstance(self.values, tuple) and all(self.values)
        singl = isinstance(self.values, str) and len(self.values) > 0
        return multi or singl


def build_data():
    """Method Doc Placeholder"""
    raw_lines = enumerate(data.readlines())
    return {id: item.upper() for id, item in raw_lines}


class BaseQueue:
    """This is the BaseObject for a Queue."""

    instruction_set = build_data()
    finished = {}
    bits = 16
    history = Logger()
    # check_list = {line.split()[-1]: [] for line in instruction_set.values()}
    check_list = {}
    ch_list_iter = 0

    def submit(self, ans_dict):
        self.check_list[self.ch_list_iter] = ans_dict
        self.ch_list_iter += 1

    @property
    def next_instruction(self):
        return self.instruction_set.pop()

    # def update_check_list(self, key, linenum):
    #     self.check_list[key].append(linenum)

    def BIN(self, n):
        """n = int()
        convert decimal n to bit sized binary string
        >>> a = BaseQueue()
        >>> a.BIN('311')
        TypeError
        >>> a.BIN(42)
        '0000000000101010'
        >>> a.BIN(500)
        '0000000111110100'
        """

        if isinstance(n, int):
            return bin(n).replace("0b", "").rjust(self.bits, "0")
        raise TypeError


class PutNotWorker(BaseQueue):
    """subclass of BaseQueue, provides generic work for
    shifter children classes."""

    # b RSHIFT 3 -> e
    # jm LSHIFT 1 -> kg
    def __init__(self):
        """init"""
        super().__init__()
        self.my_queue = {}
        self.my_outbox = {}

    def out_put(self, work_id, line_item):
        """place holder method, defined in child classes."""
        # gets replaced with:
        # def out_put(self, work_id, line_item):
        # from child class
        raise NotImplementedError("Must override out_put in Child class.")

    def work(self):
        """This is the worker function that child classes of similar
        line styles call to get their work done."""
        for work_ticket, l_item in self.my_queue.items():
            # while len(self.my_queue) > 0:
            #     job = self.my_queue.pop()

            #     work_ticket, l_item = job.items()

            # @@@@@@@@@@ delete this line when done
            # l_item = LineItem(**l_item.__dict__)

            # If it's not done, try to finish the work
            if not l_item.completed:
                # is the source address a decimal?
                if l_item.sources.isnumeric():
                    l_item.values = self.BIN(int(l_item.sources))

                # is the source address in the finished queue?
                if l_item.sources in self.finished:
                    l_item.values = self.finished[l_item.sources]

            if l_item.completed:
                # output function is defined in subclass
                self.out_put(work_ticket, l_item)

            # if it's still not done, throw it back in the queue
            else:
                # l_item.values = (left_done, right_done)
                self.my_queue[work_ticket] = l_item


class ShiftersWorker(BaseQueue):
    """subclass of BaseQueue, provides generic work for
    shifter children classes."""

    # b RSHIFT 3 -> e
    # jm LSHIFT 1 -> kg
    def __init__(self):
        """init"""
        super().__init__()
        self.my_queue = {}
        self.my_outbox = {}

    def out_put(self, work_id, line_item):
        """place holder method, defined in child classes."""
        # gets replaced with:
        # def out_put(self, work_id, line_item):
        # from child class
        raise NotImplementedError("Must override out_put in Child class.")

    def work(self):
        """This is the worker function that child classes of similar
        line styles call to get their work done."""
        for work_ticket, l_item in self.my_queue.items():
            # while len(self.my_queue) > 0:
            #     job = self.my_queue.pop()

            #     work_ticket, l_item = job.items()

            # @@@@@@@@@@ delete this line when done
            # l_item = LineItem(**l_item.__dict__)

            if l_item.completed:
                # output function is defined in subclass
                self.out_put(work_ticket, l_item)

            else:
                if not l_item.completed:
                    # is the source address a decimal?
                    if l_item.sources.isnumeric():
                        l_item.values = self.BIN(int(l_item.sources))
                    # is the source address in the finished queue?
                    if l_item.sources in self.finished:
                        l_item.values = self.finished[l_item.sources]

                # l_item.values = (left_done, right_done)
                self.my_queue[work_ticket] = l_item


class AndOrWorker(BaseQueue):
    """subclass of BaseQueue, provides generic work for
    AND and OR children classes."""

    def __init__(self):
        """init"""
        super().__init__()
        self.my_queue = {}
        self.my_outbox = {}

    def out_put(self, work_id, line_item):
        """place holder method, defined in child classes."""
        # gets replaced with:
        # def out_put(self, work_id, line_item):
        # from child class
        raise NotImplementedError("Must override out_put in Child class.")

    def work(self):
        """This is the worker function that child classes of similar
        line styles call to get their work done."""
        for work_ticket, l_item in self.my_queue.items():
            # while len(self.my_queue) > 0:
            #     job = self.my_queue.pop()

            #     work_ticket, l_item = job.items()

            if l_item.completed:
                self.out_put(work_ticket, l_item)

            else:
                left_done, right_done = l_item.values
                left_source, right_source = l_item.sources

                if not left_done:
                    # is the source address a decimal?
                    if left_source.isnumeric():
                        left_done = self.BIN(int(left_source))
                    # is the source address in the finished queue?
                    if left_source in self.finished:
                        left_done = self.finished[left_source]

                if not right_done:
                    # is the source address a decimal?
                    if right_source.isnumeric():
                        right_done = self.BIN(int(right_source))
                    # is the source address in the finished queue?
                    if right_source in self.finished:
                        right_done = self.finished[right_source]

                l_item.values = (left_done, right_done)
                self.my_queue[work_ticket] = l_item


class AndQueue(AndOrWorker):
    """Class for queueing AND jobs"""

    def __init__(self, logger):
        """init"""
        super().__init__()
        self.my_queue = {}
        self.my_outbox = {}
        self.logger = logger

        # Step 1: Populate the And Queue
        # get all the "AND" lines from instruction set
        for w_ticket, row in self.instruction_set.items():
            # ab AND ad -> ae
            # 1 AND ht -> hu
            if "AND" in row:
                first, _, second, _, target = row.split()
                new_item = LineItem(target=target, sources=(first, second))

                if target not in self.logger:
                    self.logger[target] = []
                self.logger[target].append({id: [first, second]})

                self.my_queue[w_ticket] = new_item
        self.total_jobs = len(self.my_queue)

    @property
    def progress(self):
        """How much have I got done?"""
        try:
            return len(self.my_outbox) / self.total_jobs
        except ZeroDivisionError:
            return 0

    def report(self):
        """Reporter sends back the current status of the queue"""
        return len(self.my_queue), len(self.my_outbox)

    def out_put(self, work_id, line_item):
        """This method overwrites the placeholder found in Parent class."""
        self.my_outbox[work_id] = line_item
        result = self.AND(*line_item.values)
        self.submit({line_item.target: result})
        self.finished[line_item.target] = result

    @staticmethod
    def AND(x, y):
        """
        >>> AndQueue.AND("1010101010101010", "1110111011101111")
        '1010101010101010'
        >>> AndQueue.AND('0010011001100101', '1101010000010010')
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


class OrQueue(AndOrWorker):
    """Class for queueing OR jobs"""

    def __init__(self, logger):
        """init"""
        super().__init__()
        self.my_queue = {}
        self.my_outbox = {}
        self.logger = logger

        # Step 1: Populate the OR Queue
        # get all the "OR" lines from instruction set
        for w_ticket, row in self.instruction_set.items():
            # ab OR ad -> ae
            # 1 OR ht -> hu
            if "OR" in row:
                left_val, _, right_val, _, target = row.split()
                result = LineItem(target=target, sources=(left_val, right_val))

                if target not in self.logger:
                    self.logger[target] = []
                self.logger[target].append({id: [left_val, right_val]})

                self.my_queue[w_ticket] = result
        self.total_jobs = len(self.my_queue)

    @property
    def progress(self):
        """How much have I got done?"""
        try:
            return len(self.my_outbox) / self.total_jobs
        except ZeroDivisionError:
            return 0

    def report(self):
        """Reporter sends back the current status of the queue"""
        return len(self.my_queue), len(self.my_outbox)

    def out_put(self, work_id, line_item):
        """This method overwrites the placeholder found in Parent class."""
        self.my_outbox[work_id] = line_item
        result = self.OR(*line_item.values)
        self.submit({line_item.target: result})
        self.finished[line_item.target] = result

    @staticmethod
    def OR(x, y):
        """
        >>> OrQueue.OR("1010101010101010", "1110111011101111")
        '1110111011101111'
        >>> OrQueue.OR('0010011001100101', '1101010000010010')
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


class RightQueue(ShiftersWorker):
    """Class for queueing RSHIFT jobs"""

    def __init__(self, logger):
        """init"""
        super().__init__()
        self.my_queue = {}
        self.my_outbox = {}
        self.logger = logger

        # Step 1: Populate the RSHIFT Queue
        # get all the "RSHIFT" lines from instruction set
        for w_ticket, row in self.instruction_set.items():
            # ab RSHIFT 4 -> ae
            if "RSHIFT" in row:
                source, _, count, _, target = row.split()
                self.my_queue[w_ticket] = LineItem(
                    target=target, sources=source, count=int(count)
                )

                if target not in self.logger:
                    self.logger[target] = []
                self.logger[target].append({id: [source]})

        self.total_jobs = len(self.my_queue)

    @property
    def progress(self):
        """How much have I got done?"""
        try:
            return len(self.my_outbox) / self.total_jobs
        except ZeroDivisionError:
            return 0

    def report(self):
        """Reporter sends back the current status of the queue"""
        return len(self.my_queue), len(self.my_outbox)

    def out_put(self, work_id, line_item):
        """This method overwrites the placeholder found in Parent class."""
        self.my_outbox[work_id] = line_item
        result = self.RIGHT(line_item.values, line_item.count)
        self.submit({line_item.target: result})
        self.finished[line_item.target] = result

    @staticmethod
    def RIGHT(x, n):
        """
        Shifts characters RIGHT by n places.
        displaced characters get appended to the beginning.

        >>> RightQueue.RIGHT('0010011001100101', 3)
        '1010010011001100'
        >>> RightQueue.RIGHT('0011001100101001', 5)
        '0100100110011001'
        >>> RightQueue.RIGHT('0110010100100110', 9)
        '1001001100110010'
        """
        #    00010111 (decimal +23)
        #      from ^ here
        # -> shift goes this way ->
        # =  10001011 (decimal +46)
        #    ^ goes front

        assert len(x) == 16
        assert x.isnumeric()
        assert isinstance(n, int)

        for _ in range(n):
            first, last = x[:-1], x[-1:]
            x = last + first

        assert not x.isspace()
        assert x.isnumeric()

        return x


class LeftQueue(ShiftersWorker):
    """Class for queueing LSHIFT jobs"""

    def __init__(self, logger):
        """init"""
        super().__init__()
        self.my_queue = {}
        self.my_outbox = {}
        self.logger = logger

        # Step 1: Populate the LSHIFT Queue
        # get all the "LSHIFT" lines from instruction set
        for w_ticket, row in self.instruction_set.items():
            # ab LSHIFT 4 -> ae
            if "LSHIFT" in row:
                source, _, count, _, target = row.split()
                self.my_queue[w_ticket] = LineItem(
                    target=target, sources=source, count=int(count)
                )

                if target not in self.logger:
                    self.logger[target] = []
                self.logger[target].append({id: [source]})

        self.total_jobs = len(self.my_queue)

    @property
    def progress(self):
        """How much have I got done?"""
        try:
            return len(self.my_outbox) / self.total_jobs
        except ZeroDivisionError:
            return 0

    def report(self):
        """Reporter sends back the current status of the queue"""
        return len(self.my_queue), len(self.my_outbox)

    def out_put(self, work_id, line_item):
        """This method overwrites the placeholder found in Parent class."""
        self.my_outbox[work_id] = line_item
        result = self.LEFT(line_item.values, line_item.count)
        self.submit({line_item.target: result})
        self.finished[line_item.target] = result

    @staticmethod
    def LEFT(x, n):
        """
        Shifts characters LEFT by n places.
        displaced characters get appended to the end.

        >>> LeftQueue.LEFT('0010011001100101', 3)
        '0011001100101001'
        >>> LeftQueue.LEFT('0011001100101001', 5)
        '0110010100100110'
        >>> LeftQueue.LEFT('0110010100100110', 9)
        '0100110011001010'

        """
        # 00010111 (decimal +23)
        # ^ front char
        # <- shift this way <-
        #     goes to th back
        # =  00101110 (decimal +46)
        #           ^

        assert len(x) == 16
        assert x.isnumeric()
        assert isinstance(n, int)

        for _ in range(n):
            first, last = x[:1], x[1:]
            x = last + first

        assert not x.isspace()
        assert x.isnumeric()

        return x


class NotQueue(PutNotWorker):
    """Class for queueing NOT jobs"""

    def __init__(self, logger):
        """init"""
        super().__init__()
        self.my_queue = {}
        self.my_outbox = {}
        self.logger = logger

        # Step 1: Populate the NOT Queue
        # get all the "NOT" lines from instruction set
        for w_ticket, row in self.instruction_set.items():
            # NOT 1674 -> b
            # NOT 0 -> c
            # NOT lx -> a
            if "NOT" in row:
                _, address, _, target = row.split()
                self.my_queue[w_ticket] = LineItem(
                    target=target, sources=address, values=False
                )

                if target not in self.logger:
                    self.logger[target] = []
                self.logger[target].append({id: [address]})

        self.total_jobs = len(self.my_queue)

    @property
    def progress(self):
        """How much have I got done?"""
        try:
            return len(self.my_outbox) / self.total_jobs
        except ZeroDivisionError:
            return 0

    def report(self):
        """Reporter sends back the current status of the queue"""
        return len(self.my_queue), len(self.my_outbox)

    def out_put(self, work_id, line_item):
        """This method overwrites the placeholder found in Parent class."""
        self.my_outbox[work_id] = line_item
        result = self.NOT(line_item.values)
        self.submit({line_item.target: result})
        self.finished[line_item.target] = result

    @staticmethod
    def NOT(x):
        """reverses the bits,
        what was, is no more and what wasn't, now is
        >>> NotQueue.NOT('1010101010101010')
        '0101010101010101'
        >>> NotQueue.NOT('1110111011101111')
        '0001000100010000'
        >>> NotQueue.NOT('0010011001100101')
        '1101100110011010'
        >>> NotQueue.NOT('1101010000010010')
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


class PutQueue(PutNotWorker):
    """Class for queueing PUT jobs"""

    def __init__(self, logger):
        """init"""
        super().__init__()
        self.my_queue = {}
        self.my_outbox = {}
        self.logger = logger

        # Step 1: Populate the PUT Queue
        # get all the "PUT" lines from instruction set
        for w_ticket, row in self.instruction_set.items():
            # 1674 -> b
            # 0 -> c
            # lx -> a

            # technically, PUT is not a command, it's an instruction
            # that lacks any other command.
            cmd_list = ["AND", "OR", "NOT", "RSHIFT", "LSHIFT"]
            if not bool([ele for ele in cmd_list if ele in row]):
                address, _, target = row.split()
                self.my_queue[w_ticket] = LineItem(
                    target=target, sources=address, values=False
                )

                if target not in self.logger:
                    self.logger[target] = []
                self.logger[target].append({id: [address]})

        self.total_jobs = len(self.my_queue)

    @property
    def progress(self):
        """How much have I got done?"""
        try:
            return len(self.my_outbox) / self.total_jobs
        except ZeroDivisionError:
            return 0

    def report(self):
        """Reporter sends back the current status of the queue"""
        return len(self.my_queue), len(self.my_outbox)

    def out_put(self, work_id, line_item):
        """This method overwrites the placeholder found in Parent class."""
        self.my_outbox[work_id] = line_item
        result = line_item.values
        self.submit({line_item.target: result})
        self.finished[line_item.target] = result


def solve_a(source):
    """Puzzle 1 Main Function"""
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


class MasterQueue(dict):
    """Contains all the active queues and keeps
    them working until they're done.
    Also Maintains reporting."""

    def __init__(self, target, my_log):
        self.iterations = 0
        self.target = target

    def final_answer(self):
        """and the winner is!!!"""

        final_dict = self.pop(list(self.keys())[0]).finished
        final_chek = self.pop(list(self.keys())[0]).check_list

        for i, v in final_dict.items():
            print(i, v)

        if with_examples:
            ea = example_answers
            fd = final_dict
            report = []
            a = BaseQueue()

            for key in list(ea.keys()):
                mystr = f"Wire: {key}\n"
                mystr += f"   Mine  : {fd[key]} = {int(fd[key],2)}\n"
                mystr += f"   Answer: {a.BIN(ea[key])} = {ea[key]}\n"
                mystr += "--------------------------------------------------\n"
                report.append(mystr)

            print("\n".join(report))

        else:
            finale = final_dict[self.target.upper()]

            this_try = f"Value of {self.target}: {finale} or {int(finale, 2)}"
            print(this_try)

            open("guesses.txt", "w+").writelines(this_try)

        for k, v in final_chek.items():
            print(k, v)

    def work_cycle(self):
        """method documentation placeholder"""
        self.iterations += 1
        for worker in self:
            self[worker].work()
        return self.jobs_done

    @property
    def jobs_done(self):
        """util for reporting on completeness"""
        try:
            return sum([x.progress for x in self.values()]) / len(self)
        except ZeroDivisionError:
            return 0


if __name__ == "__main__":
    this_log = Logger()
    master_queue = MasterQueue("a", this_log)
    master_queue["AND"] = AndQueue(logger=this_log)
    master_queue["OR"] = OrQueue(logger=this_log)
    master_queue["PUT"] = PutQueue(logger=this_log)
    master_queue["NOT"] = NotQueue(logger=this_log)
    master_queue["LEFT"] = LeftQueue(logger=this_log)
    master_queue["RIGHT"] = RightQueue(logger=this_log)

    print("BEFORE *****************************")

    while master_queue.jobs_done < 1:
        os.system("cls")
        master_queue.work_cycle()

        print(
            f"AFTER {master_queue.iterations} iterations *****************************"
        )
        for name, que in master_queue.items():
            left, right = que.report()
            q = f"Queue: {name}".ljust(15, " ")
            t = f"To do: {left}".ljust(15, " ")
            o = f"Outbox: {right}".rjust(15, " ")

            print(q, t, o)
    # master_queue.final_answer()

    for i, val in this_log.unique_addresses.items():
        print(i, val)
