from calendar import c
from collections import namedtuple
from dataclasses import dataclass, astuple, asdict
from random import randint

# @dataclass
class Loc:
    row: int
    col: int

    def __init__(self, row, col) -> None:
        self.row = row
        self.col = col

    def __repr__(self):
        return f'Loc("{self.row}","{self.col}")'

    def __str__(self) -> str:
        return f"({self.row},{self.col})"
    
    def __add__(self, other):
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

list_locs=[]
for _ in range(25):
    x = randint(1,10)
    y = randint(1,10)
    list_locs.append(Loc(x,y))

print(list_locs)
print(sorted(list_locs))



