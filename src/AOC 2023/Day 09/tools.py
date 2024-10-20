line_results: list = []


class Prediction:
    """Doc Placeholder text"""

    def __init__(self, page: list, running_total):
        """Doc Placeholder text"""
        line_results.append(f"{'':-^100}")
        # page is a list of integers
        # work is a list of pages, begins with original page
        work = [page]

        # fill in the extrapolated lists of all previous lists
        while not self.hit_zero(work[-1]):
            work.append(self.extrap(work[-1]))

        for line in work:
            line_results.append(f"{line}")

        # get only the last element from each list
        l_nums = [elements[-1] for elements in work][::-1]
        lastnums = [f"{x:,} " for x in l_nums]
        # ln_string =
        line_results.append(" ".join(lastnums))
        # _ = input()
        # print(line_results[-1])
        # return the sum of all the last elements.
        self.answer: int = sum(l_nums)  # l_nums[-1]
        running_total.total += self.answer
        ans_txt = " + ".join([f"{x:,}" for x in l_nums])
        line_results.append(f"Answer: {self.answer:,} = {ans_txt}")
        line_results.append(f"Running total: {running_total.total:,}")

    def hit_zero(self, test_row: list) -> bool:
        """Doc Placeholder text"""
        return sum(test_row) == 0

    def extrap(self, source_readings: list) -> list:
        """Doc Placeholder text"""
        changes = []
        for i, x in enumerate(source_readings[1:]):
            # print(i, source_readings[i])

            # version 1: get the raw difference between each element
            changes.append(x - int(source_readings[i]))
        # print(changes)
        # _ = input()
        return changes
