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

    cardinal = {
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

        # This Part just populates the coloured dict
        _ = self.get_symbols()
        _ = self.wet_targets()
        _ = self.battleship()

    def at_loc(self, row, col):
        """at_loc(y, x) -> "3"
        return value at grid reference given"""
        return self[row][col]

    def get_symbols(self):
        """returns locs for all special symbols
        found in the grid. Special characters
        are printable, non-digit, non-letter and
        not a period "." chr(46)
        """
        symbols = []
        for y, row in enumerate(self):
            for x, _ in enumerate(row):
                target_loc = (y, x)
                symbol_found = self.at_loc(*target_loc)
                if symbol_found in self.specials_chars:
                    symbols.append(target_loc)

        self.coloured["red"] = set(symbols)
        return symbols

    def adj_locs(self, row, col):
        """adj_locs(y, x) -> [(y-1,x),(y+1,x),...]
        return list of the 8 tupled grid references
        around the grid reference given."""

        surround = []
        for r, c in self.cardinal.values():
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


class SchematicPartB(list):
    """the grid"""

    # all printable non-letters, non-numbers and removed '.' (46)
    specials_chars = ["*"]

    cardinal = {
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

        # PART B ################################################
        # * loc key, val = [adjacent ships]
        self.stars_found = {}
        # PART B ################################################

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
        _ = self.get_symbols()
        _ = self.wet_targets()
        _ = self.battleship()

    def at_loc(self, row, col):
        """at_loc(y, x) -> "3"
        return value at grid reference given"""
        return self[row][col]

    def get_symbols(self):
        """returns locs for all special symbols
        found in the grid. Special characters
        are printable, non-digit, non-letter and
        not a period "." chr(46)
        """
        symbols = []
        for y, row in enumerate(self):
            for x, _ in enumerate(row):
                target_loc = (y, x)
                symbol_found = self.at_loc(*target_loc)
                if symbol_found in self.specials_chars:
                    symbols.append(target_loc)
                    self.stars_found[target_loc] = {
                        "splash": [],
                        "wet_targets": [],
                        "ships": [],
                    }

        self.coloured["red"] = set(symbols)
        return symbols

    def adj_locs(self, row, col):
        """adj_locs(y, x) -> [(y-1,x),(y+1,x),...]
        return list of the 8 tupled grid references
        around the grid reference given."""

        surround = []
        for r, c in self.cardinal.values():
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
        for s, zone in self.stars_found.items():
            area_of_effect.extend(self.adj_locs(*s))
            zone["splash"].extend(area_of_effect)

        return area_of_effect

    def wet_targets(self):
        """wet_targets(self) -> [(y,x),(y,x),...]
        Returns locs from within the AoE that are
        digits.
        """
        wt = {}  # targets within AoE

        # do this for each * individually this time
        for zone in self.stars_found.values():
            for loc in zone["splash"]:
                found = self.at_loc(*loc)
                if found.isdigit():
                    wt[loc] = found
                    zone["wet_targets"].append(loc)
            self.coloured["blue"] = set(wt.keys())
        return wt

    def battleship(self):
        """self.battleship() -> [int('467'), ...]
        goes through all the wet_targets locs and
        tries to lefty/righty find the entire
        integer found there.
        Much like the game Battleship.
        """
        # For Part B: if the PoI was a * then also dump the found
        # ships in the self.stars_found dict for that *.
        # so, since we didn't pass the PoI to battleship(),
        # we need to backwards locate the PoI to be sure.

        for star_loc, body in self.stars_found.items():
            sorted_hits = sorted(body["wet_targets"])
            checked_locs = []
            ships_found = []

            for wt in sorted_hits:

                if wt not in checked_locs:
                    # flag this loc as already checked
                    checked_locs.append(wt)

                    # start with the character we hit
                    this_ship = str(hits[wt])

                    # go left (x-n)
                    row, col = wt

                    # for visualizer
                    self.coloured["green"].add(wt)

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

                    # PART B ################################################
                    if star_flagged:
                        self.stars_found[star_loc].append(int(this_ship))
                    # PART B ################################################

                del hits[wt]
        return ships_found

    @property
    def final_answer_a(self):
        """Part A Answer"""
        return sum(self.battleship())

    @property
    def final_answer_b(self):
        """Part B Answer"""
        legal_finds = []
        for ships in self.stars_found.values():
            # find ONLY all * chars with 2 adjacent numbers
            if len(ships) == 2:
                # multiply each pair together
                legal_finds.append(math.prod(ships))

        # add those products together
        return sum(legal_finds)

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
        grid.show()
        print("Part A:".rjust(20), sep="")
        print("Ships Found:".rjust(20), colored(grid.battleship(), "green"))
        print("\n", "Part B:".rjust(20), sep="")
        # print(
        #     "Stars Found:".rjust(20),
        #     colored(list(grid.stars_found.keys()), "green"),
        # )
        print("Star Ships:".rjust(20))

        for star, ships in grid.stars_found.items():
            ship_str = ", ".join([str(ship) for ship in ships])
            print(colored(" " * 25 + f"{star}: {ship_str}", "green"))

        print("Final A Sum:".rjust(20), str(grid.final_answer_a).rjust(10))
        print("Final B Product:".rjust(20), str(grid.final_answer_b).rjust(10))

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
