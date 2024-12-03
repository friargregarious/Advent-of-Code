import pytest
import solution

@pytest.mark.parametrize("a, inst, b", [
    (45, "OR", 4),
    (43, "AND", 17),
    (25, "AND", 39),
    (7, "AND", 5),
    (49, "AND", 40),
    (15, "AND", 44),
    (20, "AND", 40),
    (7, "OR", 36),
    (26, "OR", 40),
    (1, "OR", 21),
    (29, "OR", 23),
    (20, "AND", 19),
    (46, "AND", 31),
    (3, "OR", 1),
    (34, "OR", 16),
    (21, "AND", 34),
    (24, "OR", 17),
    (12, "OR", 44),
    (34, "AND", 1),
    (24, "AND", 36),
    (38, "AND", 23),
    (37, "OR", 32),
    (27, "OR", 21),
    (32, "AND", 11),
    (16, "AND", 49),
    (4, "AND", 4),
    (31, "OR", 18),
    (5, "OR", 17),
    (3, "OR", 37),
    (31, "OR", 4),
    (26, "OR", 44),
    (35, "AND", 16),
    (2, "AND", 39),
    (44, "OR", 31),
    (47, "OR", 26),
    (37, "AND", 9),
    (16, "OR", 32),
    (28, "AND", 3),
    (47, "AND", 24),
    (7, "AND", 13),
    (39, "OR", 39),
    (15, "AND", 21),
    (29, "OR", 7),
    (22, "AND", 44),
    (7, "OR", 5),
    (12, "AND", 23),
    (36, "AND", 49),
    (48, "OR", 17),
    (20, "AND", 41),
    (39, "AND", 28),
])
def test_AND_OR(a, inst, b):
    txt_line = f"{a} {inst} {b} -> z"
    ans, instructions = {}, []
    solution.AND_OR(txt_line, ans, instructions)
    
    assert ans["z"] == a & b if inst == "AND" else a | b

