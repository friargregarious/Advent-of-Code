string = "0123456789ABCDEFGHIJKLMNOP"

col = 10
found = string[col]

print(f"Found {found} @ {col}")

for x in range(col + 5, 5, -1):
    print(string[x], "@", x)













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
