# import math
from ast import Tuple
from datetime import datetime

# from termcolor import colored
# import aocd


class Bouey:
    """Like a bouey in time, it plants itself and returns True, only
    when the given interval has elapsed."""

    flag = datetime.now()

    def __init__(self, interval: int = 0) -> None:
        self.interval = interval

    def has_elapsed(self) -> bool:
        """Returns True only once the given number of seconds has elapsed."""
        return (datetime.now() - self.flag).total_seconds() > self.interval


class Loc:
    """Recreation of a Tuple that will addition properly with others."""

    row: int
    col: int

    def __init__(self, row, col, cargo: str = "") -> None:
        self.row = row
        self.col = col
        self.cargo = cargo
        # self._id = int(datetime.now()*1000)

    def __hash__(self):
        return hash((self.row, self.col))

    def __repr__(self):
        return f"Loc(({self.row}, {self.col}) | {self.cargo})"

    def __str__(self) -> str:
        # return f"({self.row},{self.col})"
        return self.cargo

    def __value__(self):
        return (self.row, self.col)

    def __add__(self, other):
        if isinstance(other, [Tuple, list]):
            row, col = other
            return Loc(self.row + row, self.col + col)
        elif isinstance(other, Loc):
            return Loc(self.row + other.row, self.col + other.col)

    def __eq__(self, other) -> bool:
        return (self.row, self.col) == (other.row, other.col)

    def __gt__(self, other) -> bool:
        return (self.row, self.col) > (other.row, other.col)

    def __lt__(self, other) -> bool:
        return (self.row, self.col) < (other.row, other.col)

    def __lte__(self, other) -> bool:
        return (self.row, self.col) <= (other.row, other.col)

    def __gte__(self, other) -> bool:
        return (self.row, self.col) >= (other.row, other.col)


def version_increment(fname, lrg: int = 0, med: int = 0, sml: int = 0):
    newfile = []
    for row in open(fname).readlines():
        if row.startswith("__version__"):
            old_version = row.split(" = ")[1]
            lg, md, sm = old_version.strip('"').strip("'").replace('"', "").split(".")
            new_version = f'"{int(lg)+lrg}.{int(md)+med}.{int(sm)+sml}"\n'
            row = row.replace(old_version, new_version)

        newfile.append(row)
    open(fname, "w").write("".join(newfile))
