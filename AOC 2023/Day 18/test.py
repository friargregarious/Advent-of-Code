import os
# import colr
import turtle
import Solve2023_18a as slv

os.system("cls")

my_inst = slv.parse_input("example.txt")
# slv.main(my_inst)
grid = slv.map_trenches(my_inst)
grid = slv.recenter(grid)




deep, wide = slv.maximums(grid)
grid_dict = {}
for left, right in grid:
    grid_dict[left] = right

grid_dict = dict(sorted(grid_dict.items()))



# for key, val in grid_dict.items():
#     print("Dict:", key, val)

for row in range(deep + 1):
    # print(f"Row {row}: ", end="")
    for col in range(wide + 1):
        # print("X", end="")
        if (row, col) in grid_dict:
            print("#", end="")
        else:
            print(" ", end="")
    print()
# print(my_inst)
