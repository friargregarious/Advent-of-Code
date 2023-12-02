""" doc placeholder """
from datetime import datetime


class Logger(dict):
    """doc placeholder"""

    def __init__(self, logfile, inturrupts=False, print2screen=False):
        """doc placeholder"""
        self._inturrupts = inturrupts
        self._print2screen = print2screen
        self.logfile = logfile
        print(f"logger() INITIATED. {self.get_behaviours}")

    def set_behaviours(self, print2screen=False, inturrupts=False):
        """doc placeholder"""
        self._print2screen = print2screen
        self._inturrupts = inturrupts

    @property
    def get_behaviours(self):
        """doc placeholder"""
        temp = {}

        for key, val in self.__dict__.items():
            new_key = key.replace("_", "")
            temp[new_key] = val

        if self._print2screen:
            print("Conditions:", temp)
        return temp

    def save_state(self):
        """doc placeholder"""
        with open(self.logfile, "w+", encoding="UTF-8") as logfile:
            logfile.write("\n".join([x for x in self.report()]))

    def submit(self, msg):
        """doc placeholder"""
        ts = self.time_stamp
        self[ts] = msg
        self.save_state()
        if self._print2screen:
            print(ts, msg)
        if self._inturrupts:
            _ = input("Press <ENTER> to continue...")

    @property
    def time_stamp(self):
        """doc placeholder"""
        return str(datetime.now().timestamp()).replace(".", "").ljust(16,"0")
        # return datetime.now().strftime("%Y-%m-%d-%H%M%S")

    def report(self):
        """doc placeholder"""
        for time, row in self.items():
            yield f"{time} - {row}"
