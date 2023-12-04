# Advent of Code

View our [Belleville/Quinte Leader Board](https://adventofcode.com/2023/leaderboard/private/view/2588518) or [join](https://adventofcode.com/2023/leaderboard/private).

pls request a join code [from me](mailto:greg.denyes@gmail.com) to be a part of our local competition. We've changed it since last year.

## Current Year: [adventofcode.com/2023](https://adventofcode.com/2023)

- 2023 Day 01 [X][ ] Trebuchet?!
- 2023 Day 02 [X][X] Cube Conundrum
- 2023 Day 03 [X][ ] Gear Ratios 
- 2023 Day 04 [X][X] Scratchcards 


<!-- Notes
- [3]: my attempt at genetic algorithym.
- [4]: this one looks like tetris 
-->

## Previous Year's Progress

### [adventofcode.com/2022](https://adventofcode.com/2022)
- 2022 Day 01 [X][X] Calorie Counter
- 2022 Day 02 [X][X] Rock, Paper, Scissors
- 2022 Day 03 [X][X] Find the Common Item
- 2022 Day 04 [X][X] Camp Cleanup
- 2022 Day 05 [X][X] Supply Stacks
- 2022 Day 06 [X][X] Tuning Trouble
- 2022 Day 07 [_][_] No Space Left On Device
- 2022 Day 08 [X][X] Treetop Tree House
- 2022 Day 09 [X][_] Rope Bridge
- 2022 Day 10 [X][X] Cathode-Ray Tube
- 2022 Day 11 [X][_] Monkey in the Middle

### [adventofcode.com/2016](https://adventofcode.com/2016)

- 2016 Day 01 [X][X] No Time for a Taxicab
- 2016 Day 02 [X][X] Bathroom Security
- 2016 Day 03 [_][_] Squares With Three Sides

### [adventofcode.com/2015](https://adventofcode.com/2015)

- 2015 Day 01 [X][X] Not Quite Lisp
- 2015 Day 02 [X][X] I Was Told There Would Be No Math [1](#1)
- 2015 Day 03 [X][X] Perfectly Spherical Houses in a Vacuum
- 2015 Day 04 [X][X] The Ideal Stocking Stuffer [2](#2)
- 2015 Day 05 [X][X] Doesn't He Have Intern-Elves For This?
- 2015 Day 06 [X][X] Probably a Fire Hazard
- 2015 Day 07 [_][_] Some Assembly Required

[1]: *silly coder, of course there's math!*
[2]: BLOCK CHAIN HASHING!!!! YEAH!!!!

## Personal Projects

Writing a script to:

1. get year and day for selected puzzle from user
2. authenticate with adeventofcode.com
3. grab instructions & inputs for given day/year
4. create a new working folder for given day/year <-- **available in update 2022.12.10**
5. poplulate working folder with directions.md (markdown version of html from site)
6. poplulate working folder with input.txt (from site)
7. create python file from template for given day

This should be really cool, if I can figure out the OAuth1 portion of the project.

**update 2022.12.10**
get_new_day.py works... kinda
It will build a folder and working files from template using the given args from command line.

**update 2023.11.20**
I've started a new year, and so flushing out a lot of old tools. Previous 'get_new_day.py' will not work for my 2023 stuff.


<!-- `cmd
run it as:
get_new_day.py y=2022 d=19
`

it will print to screen the usage documentation without making any changes
**WARNING!!!**
double check your args when executing!!!
This prog will overwrite any files with the names:

     "description.md"
     "input.txt"
     "sample.txt"
     f"day_{day_str}.py" -->
