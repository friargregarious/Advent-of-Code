

for character in [".", "\\", "/", "|", "-"]:
    print(character,"=", ord(character))




# from random import randint, choice
# import Solve2023_16a

# NORTH = (-1, 0)
# SOUTH = (+1, 0)
# EAST = (0, +1)
# WEST = (0, -1)


# class Mover:
#     def __init__(self, *args) -> None:
#         self.row, self.col = args
#         self.direction = EAST

#     def set_dir(self, dir: tuple):
#         self.direction = dir

#     def __repr__(self) -> str:
#         return f"Mover({self.row}, {self.col}) -> {self.direction}"


# cardinal = [NORTH, SOUTH, EAST, WEST]
# my_movers = [Mover(randint(0, 20), randint(0, 20)) for _ in range(20)]

# for x in my_movers:
#     x.set_dir(choice(cardinal))

# for x in my_movers:
#     print(repr(x))
