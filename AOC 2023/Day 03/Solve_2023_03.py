"""
###############################################################################
#
#                              ADVENT OF CODE: 2023
#                                  Gear Ratios
#                      https://adventofcode.com/2023/day/3
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
"""
import os
import math
from termcolor import colored

# data = open("example.txt").read().split("\n")
# data = open("input.txt").read().split("\n")
###############################################################################
# {example 1}


class SchematicPartA(list):
    """the grid"""

    # all printable non-letters, non-numbers and removed '.' (46)
    specials_chars = [
        chr(x)
        for x in range(0, 128)
        if (
            chr(x).isprintable()
            and not chr(x).isalpha()
            and not chr(x).isdigit()
            and x != 46
        )
    ]  # this is good

    CARDINAL = {
        "up": (-1, 0),
        "upright": (-1, +1),
        "right": (0, +1),
        "downright": (1, +1),
        "down": (1, 0),
        "downleft": (1, -1),
        "left": (0, -1),
        "upleft": (-1, -1),
    }

    def __init__(self, data_list):
        """where shit gets started"""

        for row in data_list:
            this_row = row.strip("\n")
            self.max_wide = len(this_row)
            self.append(this_row)  # .split()
        self.max_high = len(self)

        self.legal_locations = set()
        for y in range(self.max_high):
            for x in range(self.max_wide):
                self.legal_locations.add((y, x))

        self.coloured = {
            "red": set(),
            "green": set(),
            "blue": set(),
        }  # 000:[(x,y),(x,y),(x,y)]

        self.symbols_found = {}

        # This Part just populates the coloured dict
        _ = self.get_symbols()
        _ = self.wet_targets()
        _ = self.battleship()

    def at_loc(self, row, col):
        """at_loc(y, x) -> "3"
        return value at grid reference given"""
        return self[row][col]

    # def get_symbols(self):
    #     """returns locs for all special symbols
    #     found in the grid. Special characters
    #     are printable, non-digit, non-letter and
    #     not a period "." chr(46)
    #     """
    #     symbols = []
    #     for y, row in enumerate(self):
    #         for x, _ in enumerate(row):
    #             target_loc = (y, x)
    #             symbol_found = self.at_loc(*target_loc)
    #             if symbol_found in self.specials_chars:
    #                 symbols.append(target_loc)

    #     self.coloured["red"] = set(symbols)
    #     return symbols

    def adj_locs(self, row, col):
        """adj_locs(y, x) -> [(y-1,x),(y+1,x),...]
        return list of the 8 tupled grid references
        around the grid reference given."""

        surround = []
        for r, c in CARDINAL.values():
            new_loc = (row + r, col + c)
            if new_loc in self.legal_locations:
                surround.append(new_loc)
        return surround

    def splash_zone(self):
        """splash_zone(self) -> [(y,x),(y,x),...]
        returns locations within range of
        the Points of Impact (PoI's).
        The ENTIRE AREA EFFECTED!
        """
        area_of_effect = []  # AoE
        for s in self.get_symbols():
            area_of_effect.extend(self.adj_locs(*s))
        return area_of_effect

    def wet_targets(self):
        """wet_targets(self) -> [(y,x),(y,x),...]
        Returns locs from within the AoE that are
        digits.
        """
        wt = {}  # targets within AoE
        for loc in self.splash_zone():
            found = self.at_loc(*loc)
            if found.isdigit():
                wt[loc] = found
        self.coloured["blue"] = set(wt.keys())
        return wt

    def battleship(self):
        """self.battleship() -> [int('467'), ...]
        goes through all the wet_targets locs and
        tries to lefty/righty find the entire
        integer found there.
        Much like the game Battleship.
        """

        hits = self.wet_targets()
        sorted_hits = sorted(hits)
        checked_locs = []
        ships_found = []

        for gz in sorted_hits:
            if gz not in checked_locs:
                # flag this loc as already checked
                checked_locs.append(gz)

                # start with the character we hit
                this_ship = str(hits[gz])

                # go left (x-n)
                row, col = gz

                # for visualizer
                self.coloured["green"].add(gz)

                PoI = col
                # reverse range indexes suck donkey
                # for x in range(col - 1, -1, -1):
                while True:
                    PoI -= 1

                    if (row, PoI) not in self.legal_locations:
                        break  # we've hit the start

                    search_loc = (row, PoI)
                    content_left = self.at_loc(*search_loc)

                    not_water = content_left != "."
                    is_digit = content_left.isdigit()
                    not_checked = search_loc not in checked_locs

                    if all([not_water, is_digit, not_checked]):
                        self.coloured["green"].add(search_loc)
                        checked_locs.append(search_loc)
                        this_ship = content_left + this_ship
                        continue

                    break  # stop looking, we don't need anymore.

                # go right (x+1)
                PoI = col
                # for x in range(col + 1, self.max_wide):
                while True:
                    PoI += 1

                    if (row, PoI) not in self.legal_locations:
                        break  # we've hit the end

                    search_loc = (row, PoI)
                    content_right = self.at_loc(*search_loc)

                    not_checked = search_loc not in checked_locs
                    is_digit = content_right.isdigit()
                    not_water = content_right != "."

                    if all([not_water, is_digit, not_checked]):
                        self.coloured["green"].add(search_loc)
                        checked_locs.append(search_loc)
                        this_ship += content_right
                        continue

                    break  # stop looking, we don't need anymore.

                ships_found.append(int(this_ship))

            del hits[gz]
        return ships_found

    @property
    def final_answer_a(self):
        """Part A Answer"""
        return sum(self.battleship())

    def show(self):
        """Prints the grid to screen"""
        os.system("cls")
        # print("Reds:", self.coloured["red"])
        # print("Greens:", self.coloured["green"])
        # print("Blues:", self.coloured["blue"])
        # _ = input("Press <ENTER> to continue:".center(80))

        for y, row in enumerate(self):
            row_content = str(y).rjust(5, "0") + " - "
            for x, _ in enumerate(row):
                # if self.at_loc(y, x):

                if (y, x) in self.coloured["red"]:  # get_symbols():
                    row_content += colored(self.at_loc(y, x), "red")

                elif (y, x) in self.coloured["green"]:  # .battleship():
                    row_content += colored(self.at_loc(y, x), "green")

                elif (y, x) in self.coloured["blue"]:  # .wet_targets():
                    row_content += colored(self.at_loc(y, x), "blue")

                else:
                    row_content += self.at_loc(y, x)

            print(row_content)
        print("\n\n")  # end of page
        # _ = input("Press <ENTER> to continue:".center(80))


CARDINAL = {
    "up": (-1, 0),
    "upright": (-1, +1),
    "right": (0, +1),
    "downright": (1, +1),
    "down": (1, 0),
    "downleft": (1, -1),
    "left": (0, -1),
    "upleft": (-1, -1),
}


class SchematicPartB(list):
    """the grid"""

    # all printable non-letters, non-numbers and removed '.' (46)
    specials_chars = ["*"]

    def __init__(self, data_list):
        """where shit gets started"""

        for row in data_list:
            this_row = row.strip("\n")
            self.max_wide = len(this_row)
            self.append(this_row)  # .split()
        self.max_high = len(self)

        self.legal_locations = set()
        for y in range(self.max_high):
            for x in range(self.max_wide):
                self.legal_locations.add((y, x))

        self.symbols_found = {}
        self.ships_found = {}
        self.searched_cells = set()

    def is_legal_loc(self, loc):
        """simple guide to staying inside the grid"""
        return loc in self.legal_locations

    def at_loc(self, loc):
        """at_loc(y, x) -> "3"
        return value at grid reference given"""
        row, col = loc
        return self[row][col]

    def adj_locs(self, loc):
        """adj_locs(y, x) -> [(y-1,x),(y+1,x),...]
        Adjacent Locations: return list of the 8 tupled
        grid references around the grid reference given.
        """
        row, col = loc

        surround = []
        for r, c in CARDINAL.values():
            new_loc = (row + r, col + c)
            if new_loc in self.legal_locations:
                surround.append(new_loc)
        return surround

    @property
    def final_answer_b(self):
        """Part B Answer"""
        legal_finds = []

        for ships in self.symbols_found.values():
            # find ONLY all * chars with 2 adjacent numbers
            if len(ships) == 2:
                # multiply each pair together
                legal_finds.append(math.prod(ships))

        # add those products together
        return sum(legal_finds)


###############################################################################
# end of functions
###############################################################################


def show(self):
    """Prints the grid to screen"""
    os.system("cls")
    # print("Reds:", self.coloured["red"])
    # print("Greens:", self.coloured["green"])
    # print("Blues:", self.coloured["blue"])
    # _ = input("Press <ENTER> to continue:".center(80))

    for y, row in enumerate(self):
        row_content = str(y).rjust(5, "0") + " - "
        for x, _ in enumerate(row):
            # if self.at_loc(y, x):

            # if (y, x) in self.coloured["red"]:  # get_symbols():
            #     row_content += colored(self.at_loc(y, x), "red")

            # elif (y, x) in self.coloured["green"]:  # .battleship():
            #     row_content += colored(self.at_loc(y, x), "green")

            # elif (y, x) in self.coloured["blue"]:  # .wet_targets():
            #     row_content += colored(self.at_loc(y, x), "blue")

            # else:
            # row_content += self.at_loc(y, x)
            row_content += self.at_loc((y, x))

        print(row_content)
    print("\n\n")  # end of page
    # _ = input("Press <ENTER> to continue:".center(80))


def get_symbols(grid_obj):
    """returns locs for all special symbol_locs found in the grid. Special
    characters are found in the grid_object.specials() list
    """

    symbol_locs = {}
    for y, row in enumerate(grid_obj):
        for x, _ in enumerate(row):
            target_loc = (y, x)
            symbol_found = grid_obj.at_loc(target_loc)
            if symbol_found in grid_obj.specials_chars:
                if symbol_found not in symbol_locs:
                    symbol_locs[symbol_found] = []
                symbol_locs[symbol_found].append(target_loc)

    return symbol_locs


def get_wets_for_stars(grid_obj):
    """I asked Perplexity for some help. Sue me."""
    numbers_for_stars = {}

    for star_loc in grid_obj.symbols_found["*"]:
        numbers = []
        for loc in grid_obj.adj_locs(star_loc):
            value = grid_obj.at_loc(loc)
            if value.isdigit():
                numbers.append(loc)

        numbers_for_stars[star_loc] = numbers
    return numbers_for_stars


def battleship(grid_obj, wets_found):
    """finds digits from symbols_found and stores them in ships_found"""
    # input:
    # self.symbols_found = {
    #     (special char loc):[(wet, loc),(wet, loc),(wet, loc),(wet, loc)]
    #     }

    # returns:
    # self.ships_found = {
    #     (special char loc):[456, 654]
    #     }

    # searched_cells.add(search_loc)
    total_finds = []
    for star_loc, adjacent_locs in wets_found.items():
        legal_finds = []
        for adj_loc in adjacent_locs:
            if adj_loc not in grid_obj.searched_cells:
                legal_finds.append(whole_number(grid_obj, adj_loc))

        sit_rep = {star_loc: legal_finds}
        grid_obj.ships_found.update(sit_rep)
        total_finds.extend(legal_finds)

    return total_finds


def whole_number(grid_obj, anchor_point=(0, 0)):
    """grid_obj.battleship() -> [int('467'), ...]
    returns an integer of the entire number located
    from the anchor_point.
    """

    # this is the wet location we start with.
    num_word = grid_obj.at_loc(anchor_point)
    searched_cells = set()

    # from here we go left to find the begining of the number
    while True:
        # take one step left and look at it
        row, point_of_interest = anchor_point
        point_of_interest -= 1
        search_loc = (row, point_of_interest)
        if not grid_obj.is_legal_loc(search_loc):
            break  # point of interest is beyond scope of grid

        content_left = grid_obj.at_loc(search_loc)

        if content_left.isdigit():
            num_word = content_left + num_word
            searched_cells.add(search_loc)
            continue

        break  # stop looking, we don't need anymore.

    # go right (x+1)
    # then we go right to find the end

    while True:
        # take one step right and look at it
        row, point_of_interest = anchor_point
        point_of_interest += 1
        search_loc = (row, point_of_interest)
        if not grid_obj.is_legal_loc(search_loc):
            break  # point of interest is beyond scope of grid

        content_right = grid_obj.at_loc(search_loc)

        if content_right.isdigit():
            num_word += content_right
            searched_cells.add(search_loc)
            continue

        break  # stop looking, we don't need anymore.

    # all the searched cells need to be added to the
    # global search list for the next num_word we look for.
    for cell in searched_cells:
        self.searched_cells.add(cell)

    # return an int() of the complete number
    return int(num_word)


###############################################################################
# end of functions
###############################################################################


def solve_a(source, show_work=False):
    """finds any number touching a strange symbol
    then returns the sum of found numbers"""
    grid = SchematicPartA(source)
    if show_work:
        grid.show()
        print("\n\n")
        print("Ships Found:".rjust(20), colored(grid.battleship(), "green"))
        print("Final A Sum:".rjust(20), str(grid.final_answer_a).rjust(10))

    return grid.final_answer_a


###############################################################################
# {example 2}


def solve_b(source, show_work=False):
    """The missing part wasn't the only issue - one of the gears in the engine
    is wrong. A gear is any * symbol that is adjacent to exactly two part
    numbers. Its gear ratio is the result of multiplying those two numbers
    together.

    This time, you need to find the gear ratio of every gear and add them all
    up so that the engineer can figure out which gear needs to be replaced.
    """

    grid = SchematicPartB(source)
    if show_work:
        show(grid)
        print("\n", "Part B:".rjust(20), sep="")
        print("Star Ships:".rjust(20), )

        grid.symbols_found = get_symbols(grid)
        splashed_targets = get_wets_for_stars(grid)
        print("Splashed:", splashed_targets)
        for star, wet_nums in splashed_targets.items():
            nums_found = []
            for wet_loc in wet_nums:
                nums_found.append(whole_number(grid, wet_loc))

            ship_list = ", ".join([str(x) for x in nums_found])
            print("STAR:", star, "WET LOCS:", ship_list)

    return grid.final_answer_b


###############################################################################
# ENTRY POINT FOR SUBMITTING & BENCHMARKING


def main(source):
    """tescts"""
    return (solve_a(source=source), solve_b(source=source))


if __name__ == "__main__":
    os.system("cls")
    # data = open("example.txt", encoding="UTF-8").read().split("\n")
    data = open("gregexample.txt", encoding="UTF-8").read().split("\n")
    # data = open("input.txt", encoding="UTF-8").read().split("\n")
    solve_b(data, show_work=True)

    # if using gregexample.txt, the answer is (10 x 10) + (10 x 10)
    # from locs (9, 27) & (13, 10)
    # (5, 22) is actually touching 3 numbers so it shouldn't be picked
