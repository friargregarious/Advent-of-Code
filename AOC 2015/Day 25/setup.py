# import os
from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

# Your own solutions can be executed by writing and using an entry-point
# into your code, registered in the group "adventofcode.user". Your entry-
# point should resolve to a callable, and it will be called with three keyword
# arguments: year, day, and data. For example, my entry-point is called "wim"
# and running against my code (after pip install advent-of-code-wim) would be
# like this:

# https://github.com/wimglenn/advent-of-code-sample

# setup(
#     ...
#     entry_points={"adventofcode.user": ["myusername = mypackage:mysolve"]},
# )


setup(
    name="Solve_2015_25",
    entry_points={
        "adventofcode.user": [
            "friargregarious = Solve_2015_25:main",
        ],
    },
)


# os.chdir("C:\\GitHub\\Solve_2015_25\\app_v1_0")

# build the executable
os.system("pyinstaller --onefile Solve_2015_25.py")
