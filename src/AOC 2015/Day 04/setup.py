import os
from setuptools import setup


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
    name="Solve_2015_04",
    entry_points={
        "adventofcode.user": [
            "friargregarious = Solve_2015_04:main",
        ],
    },
)


# os.chdir("C:\\GitHub\\Solve_2015_04\\app_v1_0")

# build the executable
os.system("pyinstaller --onefile Solve_2015_04.py")
