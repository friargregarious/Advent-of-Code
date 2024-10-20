"""Module providing a function printing python version."""
from Solve_2015_07 import Circuit

work = Circuit()
file = enumerate(open("input.txt", "r", encoding="UTF-8").readlines())
unprocessed = {str(ln + 1).rjust(4, "0"): line for ln, line in file}


def test_submit():
    """Function printing python version."""
    inc, c_not, c_and, c_rshift, c_or, c_lshift = 0, 0, 0, 0, 0, 0

    for k, line in unprocessed.items():
        assert work.to_do == inc
        if "NOT" in line:
            c_not += 1
        if "RSHIFT" in line:
            c_rshift += 1
            c_not += 1
            c_and += 1
            c_lshift += 1
            c_or += 1

        work.submit(k, line)

        if "NOT" in line:
            assert len(work.instructions["NOT"]) == c_not
        if "RSHIFT" in line:
            assert len(work.instructions["RSHIFT"]) == c_not
