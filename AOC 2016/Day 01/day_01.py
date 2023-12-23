import sys
SAMPLE = "sample" in sys.argv
TEST = "test" in sys.argv


source = "input.txt"
if SAMPLE:
    source = "sample.txt"


DIRS = {
    0: "NORTH",
    90: "EAST",
    180: "SOUTH",
    270: "WEST",
    "L": "LEFT",
    "R": "RIGHT"

}


class Walker:
    def __init__(self):
        self.direction = 0 ## start facing NORTH
        self._x = 0
        self._y = 0
        self.odometer = 0

        print(
            f"""INIT:\tWalker initialized 
            located {self.loc} 
            facing {self.facing} 
            distance traveled {self.odometer}.
            """)

    @property
    def facing(self):
        return DIRS[self.direction]

    @property
    def loc(self):
        return (self._x, self._y,)

    def status(self):

        print(
            f"""STATUS:\tWalker Ready 
            located {self.loc} 
            facing {self.facing} 
            distance traveled {self.odometer}.
            """)

    def execute(self ,entry):
        direction = entry[0]
        distance = int(entry[1:])
        turned = self.turn(direction)
        traveled = self.travel(distance)
        return turned, *traveled

    def turn(self, direction):
        if direction == "R": # turning right adds 90 to current direction
            self.direction += 90
            if self.direction >= 360:
                self.direction -= 360

        elif direction == "L": # turning left subtracts 90 from current direction
            self.direction -= 90
            if self.direction < 0:
                self.direction += 360

        return f"Turned {DIRS[direction]}, now facing {DIRS[self.direction]}"

    def travel(self, distance):
        startingpoint = str(self.loc)
        move_me = distance
        steps = []

        if self.facing in ["WEST", "SOUTH"]:
            move_me = -1
        else:
            move_me = 1

        if self.facing in ["NORTH", "SOUTH"]:  # y axis movement
            for i in range(1, 1 + distance):
                self._y += move_me
                steps.append(self.loc)

        elif self.facing in ["EAST", "WEST"]:  # x axis movement
            for i in range(1, 1 + distance):
                self._x += move_me
                steps.append(self.loc)

        if str(self.loc) == startingpoint:
            return f"Failed to travel!!!"

        self.odometer += distance
        return f"Traveled {self.facing} for {distance} blocks from {startingpoint} to {self.loc}.", steps


def revamp_route(from_spot, to_spot):
    # from always starts at (0,0)

    from_x, from_y = 0, 0
    to_x, to_y = to_spot

    distance = (abs(to_y) + from_y) + (abs(to_x)+from_x)
    return distance



if __name__ == "__main__":
    data = str(
        open(source).read()
        ).strip().split(", ")

    if TEST:
        santa = Walker()
        print(santa.travel(2))
        print(santa.turn("R"))
        print(santa.travel(2))
        print(santa.turn("R"))
        print(santa.travel(2))
        print(santa.turn("R"))
        print(santa.travel(2))

        santa.status()

        print(santa.travel(2))
        print(santa.turn("L"))
        print(santa.travel(2))
        print(santa.turn("L"))
        print(santa.travel(2))
        print(santa.turn("L"))
        print(santa.travel(2))

        santa.status()


    else:
        santa = Walker()
        starting = santa.loc

        sites_visited = []

        for entry in data:
            turn_msg, dir_msg, steps_taken = santa.execute(entry)
            # print(msg)
 
            print(f"Steps taken this turn: {steps_taken}")
            for step in steps_taken:
                if step in sites_visited:
                    print(f"Actual site is at {step}.")
                    print(f"Distance to actual site is {revamp_route(starting, step)}.")
                    sys.exit()
                else:
                    sites_visited.append(step)

        ending = santa.loc
        santa.status()
        print(
            f"total direct distance between points: {revamp_route(starting, ending)} ")
