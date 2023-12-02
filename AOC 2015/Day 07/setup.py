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
    name="Solve_2015_07",
    version="0.1",
    description="Advent of Code Solution for Puzzle 2015 Day 7.",
    long_description="readme.md",
    long_description_content_type="text/markdown",
    author="friargregarious",
    author_email="greg.denyes@gmail.com",
    entry_points={
        "adventofcode.user": [
            "friargregarious = Solve_2015_07:main",
        ],
    },
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # Indicate who your project is intended for
        "Intended Audience :: Puzzle Hackers",
        "Topic :: Software Development :: Build Tools",
        # Pick your license as you wish
        "License :: OSI Approved :: MIT License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
)


# os.chdir("C:\\GitHub\\Solve_2015_07\\app_v1_0")

# build the executable
os.system("pyinstaller --onefile Solve_2015_07.py")
