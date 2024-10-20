import os

book = [[10, 13, 16, 21, 30, 45]]  # ansr is 68


class Prediction:
    """Doc Placeholder text"""

    def __init__(self, page: list):
        """Doc Placeholder text"""
        work = [page]
        while not self.hit_zero(work[-1]):
            work.append(self.extrap(work[-1]))
        self.answer = sum([x[-1] for x in work][::-1])

    def hit_zero(self, test_row: list):
        """Doc Placeholder text"""
        return sum(test_row) == 0

    def extrap(self, source_readings: list):
        """Doc Placeholder text"""
        changes = []
        for i, x in enumerate(source_readings[1:]):
            # print(i, source_readings[i])
            changes.append(x - int(source_readings[i]))
        return changes


# mybooks = [[0, 3, 6, 9, 12, 15], [1, 3, 6, 10, 15, 21], [10, 13, 16, 21, 30, 45]]
mybooks = [
    [
        8,
        27,
        61,
        121,
        232,
        446,
        858,
        1625,
        2988,
        5297,
        9039,
        14869,
        23644,
        36460,
        54692,
        80037,
        114560,
        160743,
        221537,
        300417,
        401440,
    ],
    [
        8,
        8,
        3,
        -9,
        -26,
        -26,
        63,
        410,
        1348,
        3464,
        7715,
        15573,
        29202,
        51670,
        87199,
        141456,
        221888,
        338104,
        502307,
        729779,
        1039422,
    ],
    [
        7,
        20,
        43,
        80,
        131,
        192,
        255,
        308,
        335,
        316,
        227,
        40,
        -277,
        -760,
        -1449,
        -2388,
        -3625,
        -5212,
        -7205,
        -9664,
        -12653,
    ],
]

os.system("cls")
my_predictions = [Prediction(page).answer for page in mybooks]
print("My Predictions:", my_predictions)
for pgnum, page in enumerate(mybooks):
    print(f"The answer to #{pgnum} is: [{Prediction(page).answer:,}]".ljust(35), page[::-1])

print("The final Solution:", sum(my_predictions))
