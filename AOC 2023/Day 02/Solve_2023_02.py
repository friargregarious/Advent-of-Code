###############################################################################
#
#                              ADVENT OF CODE: 2023
#                                 Cube Conundrum
#                      https://adventofcode.com/2023/day/2
#
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
raw = open("input.txt", encoding="UTF-8").read().split("\n")
# raw = open("example.txt", encoding="UTF-8").read().split("\n")
# data = [row for row in raw if row.isalnum()]
data = list(raw)
# print(data)
###############################################################################
# {example 1}

limits = {"red": 12, "blue": 14, "green": 13}
results = {}

# class Game(dict):
#     def __init__(self, game_str):
#         self.game_str = game_str


#     def 





def solve_a(source):
    """determine how many games from the data list would be possible
    based on the limits provided."""

    # limits = 
    results = {}

    for row in data:
        if len(data) > 5:
            game_id, game_data = row.split(": ")
            results[game_id] = {"red": [], "green": [], "blue": []}

            for rounds in game_data.split("; "):
                print("Round:", rounds)
                for colour in rounds.split(", "):
                    qty, clr = colour.split(" ")
                    print("qty:", qty, "colour", clr)
                    results[game_id][clr].append(int(qty))
            print(results[game_id])
    solution = {}
    for game_id, colours in results.items():
        solution[game_id] = {"red": None, "green": None, "blue": None}
        for this_colour, res in colours.items():
            print(max(res) < limits[this_colour], max(res), limits[this_colour])
            answer = max(res) < limits[this_colour]
            solution[game_id][this_colour] = answer


    summer = 0
    for game_id, totals in solution.items():
        print(game_id, totals, "Possible:", all(totals.values()))
        if all(totals.values()):
            summer += int(game_id.split(" ")[1])
    print("final answer:", summer)
    return solution


###############################################################################
# {example 2}


def solve_b(source):
    return solution


###############################################################################
# ENTRY POINT FOR SUBMITTING & BENCHMARKING


def main(source):
    return (solve_a(source=source), solve_b(source=source))


if __name__ == "__main__":
    solve_a(data)
