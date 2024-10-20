import sys

TEST = "test" in sys.argv
VERBOSE = "verbose" in sys.argv
PART2 = "part2" in sys.argv

answer = {}

if TEST:
    source_file = "sample.txt"
else:
    source_file = "input.txt"

answer = {"sample": "1985", "part2": "5DB3", "final": ""}

source = list(open(source_file).readlines())

# Each line of instructions corresponds to one button,
# starting at the previous button
# (or, for the first line, the "5" button)

if not PART2:
    BUTTON_GRID = [
        [x for x in range(1, 4)],
        [x for x in range(4, 7)],
        [x for x in range(7, 10)],
    ]

    B_RIGHT = [3, 6, 9]
    B_LEFT = [1, 4, 7]
    B_HIGH = [1, 2, 3]
    B_LOW = [7, 8, 9]

else:
    # PART2

    BUTTON_GRID = [
        [[" "], [" "], ["1"], [" "], [" "]],
        [[" "], ["2"], ["3"], ["4"], [" "]],
        [["5"], ["6"], ["7"], ["8"], ["9"]],
        [[" "], ["A"], ["B"], ["C"], [" "]],
        [[" "], [" "], ["D"], [" "], [" "]],
    ]

    #       1
    #     2 3 4
    #   5 6 7 8 9
    #     A B C
    #       D

def out_of_range(loc):
    y, x = loc
    UNUSABLE = [(0, 0), (0, 1), (0, 3), (0, 4), (1, 0), (1, 4),
                (3, 0), (3, 4), (4, 0), (4, 1), (4, 3), (4, 4)]

    return (y in [-1, 5]) or (x in [-1, 5]) or (loc in UNUSABLE)

P2_BUTTONS = {
    (0, 2): "1",
    (1, 1): "2",
    (1, 2): "3",
    (1, 3): "4",
    (2, 0): "5",
    (2, 1): "6",
    (2, 2): "7",
    (2, 3): "8",
    (2, 4): "9",
    (3, 1): "A",
    (3, 2): "B",
    (3, 3): "C",
    (4, 2): "D",
}

# You still start at "5" and stop when you're at an edge, 
# but given the same instructions as above, the outcome is very different
CENTER_BUTTON = (2, 0)

if __name__ == "__main__":

    if not PART2:
        last_button_pressed = 5  # default starting location
        finger_over_button = 5

        for this_button in source:
            # print(this_button)
            for move in this_button.strip():
                print(f"Moving to button {move}")
                # U moves up
                if move == "U":
                    if finger_over_button not in B_HIGH:
                        finger_over_button -= 3

                # D moves down
                elif move == "D":
                    if finger_over_button not in B_LOW:
                        finger_over_button += 3

                # L moves left
                elif move == "L":
                    if finger_over_button not in B_LEFT:
                        finger_over_button -= 1

                # R moves right
                elif move == "R":
                    if finger_over_button not in B_RIGHT:
                        finger_over_button += 1

                else:
                    print("Instruction not currently within our capabilities.")
                    sys.exit()

            # press whatever button you're on at the end of each line
            answer["final"] += str(finger_over_button)
            last_button_pressed = finger_over_button
    else:
        last_button_pressed = CENTER_BUTTON  # default starting location
        finger_over_button = CENTER_BUTTON

        for this_button in source:
            # print(this_button)
            for move in this_button.strip():
                row, col = finger_over_button
                print(f"Moving to button {move}",end=" ")

                # U moves up
                if move == "U":
                    target_button = (row - 1, col,)
                # D moves down
                elif move == "D":
                    target_button = (row + 1, col,)
                # L moves left
                elif move == "L":
                    target_button = (row, col - 1,)
                # R moves right
                elif move == "R":
                    target_button = (row, col + 1,)
                else:
                    print("Instruction not currently within our capabilities.")
                    sys.exit()

                if not out_of_range(target_button):
                    y, x = target_button
                    finger_over_button = (y, x,)
                    print(P2_BUTTONS[finger_over_button])
                else:
                    print(f"That button is blank")

            # press whatever button you're on at the end of each line
            answer["final"] += P2_BUTTONS[finger_over_button]
            last_button_pressed = finger_over_button

    print(answer["final"], answer["final"] == answer["sample"])
