import imp

    # load a source module from a file
    file, pathname, description = imp.find_module(
        "reporting", [root + "/my_utilities/"]
    )
    
    reporting = imp.load_module("my_module", file, pathname, description)

    import sys

    # cfg = ConfigParser()
    # MY_ENV = "././.env"
    MY_UTIL = "././my_utilities/"
    sys.path.append(MY_UTIL)
    from reporting import test_puzzle_report as test_report

    # cfg.read("C:/Advent of Code/.env")
    # cfg.read(MY_ENV)
    # util_path = cfg.get(section="paths", option="utilities")

    # "C:\Advent of Code\my_utilities"

    year = 2023
    day = 8
    correct_example_a = 6
    correct_example_b = 6

    EXAMPLE = True
    # EXAMPLE = False
    test_report(year, day, EXAMPLE, correct_example_a, correct_example_b)
import imp


# load a source module from a file
file, pathname, description = imp.find_module(
    "reporting", [root + "/my_utilities/"]
)

reporting = imp.load_module("my_module", file, pathname, description)



year = 2023
day = 8
correct_example_a = 6
correct_example_b = 6

EXAMPLE = True
# EXAMPLE = False
test_report(year, day, EXAMPLE, correct_example_a, correct_example_b)
