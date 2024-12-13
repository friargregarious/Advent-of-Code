"""
################################################################################
#                                                                              #
#                             ADVENT OF CODE: 2024                             #
#                                Garden Groups                                 #
#                     https://adventofcode.com/2024/day/12                     #
#                                                                              #
################################################################################
#                                                                              #
# A SOLVED:   2024-12-12 16:34                                                 #
# SOLVER:     friargregarious (greg.denyes@gmail.com)                          #
# HOME:       https://github.com/friargregarious                               #
#                                                                              #
#                   WRITTEN AND TESTED IN PYTHON VER 3.13.0                    #
#                                                                              #
################################################################################
"""
###############################################################################
# imports, globals and helper functions/classes

from numpy import around
import os, argparse, toml, sys
import solve_utilities as su
from pathlib import Path

MAX_ROWS:int = 0
MAX_COLS:int = 0

def draw_region(region, garden):
    
    for r in range(0, MAX_ROWS):
        row = []
        for c in range(0, MAX_COLS):
            
            if (r, c) in region:
                row.append( garden[(r, c)])
            else:
                row.append(".")
            
        print("".join(row))
        



def data(input_text_path:Path=Path("input.txt")):
    text_source_list = input_text_path.read_text(encoding="UTF-8").split("\n")

    global MAX_ROWS, MAX_COLS
    MAX_ROWS = len(text_source_list)
    MAX_COLS = len(text_source_list[0])

    garden = {}

    for r, row in enumerate(text_source_list): 
        for c, item in enumerate(row):
            garden[(r,c)] = item  # saving VEGI TYPE to coordinates
    
    return garden


###############################################################################
# PART A
###############################################################################



VEG_TYPE = 0
REGION = 1
PLOT_NEIGHBOR = 2

def build_plots(garden:dict):
    plots:dict = {}  # individual locs of veggies
    regions:dict = {}  # area of multiple plots of similar veggies

    # plot_loc  = { 
    #              "veg" : "",  
    #              "region" : 0,  
    #              "plot_neighbors" : [], 
    #              }

    # veg:, address, member_of)
    for loc, veg in garden.items():
        plots[loc] = {
            "veg" : veg,
            "region" : None,
            "plot_neighbors" : su.around_me(loc, garden),  # list of locs for neighbors with same veg type
        }

        for neighbor in su.around_me(loc, garden):
            if neighbor not in plots:
                plots[neighbor] = {
                    "veg" : garden[neighbor],
                    "region" : None,
                    "plot_neighbors" : [],
                }

        related = plots[loc]["plot_neighbors"] + [loc]
        found_region = False
        for region in regions:
            if set(related).intersection(regions[region]):
                found_region = True
                for l in related:
                    plots[l]["region"] = region
                    regions[region].add(l)
                break

        if not found_region:
            new_region = len(regions) + 1
            regions[new_region] = set(related)
            for l in related:
                plots[l]["region"] = new_region

    
    # NOW WE NEED TO MERGE REGIONS THAT MISTAKENLY SEPARATE
    for reg, these_locs in regions.items():
        other_regions = [r for r in regions.keys() if r != reg]
        for r in other_regions:
            other_locs = regions[r]
            if set(these_locs).intersection(other_locs):
                regions[reg] = set(these_locs).union(other_locs)
                regions[r].clear()
                # NOW WE NEED TO FIX THE PLOTS NEIGHBOR COUNTS
                for l in regions[reg]:
                    plots[l]["plot_neighbors"] = su.around_me(l, garden)
                    if l == (0,8):
                        print("Why this come up as 4? --> ", l, plots[l]["plot_neighbors"])
                        
                break


    return plots, regions




def solve_a(garden:dict):
    """for solving Part A"""
    print("\n\n{'*' * 60} Part A\n\n")
    
    plots, regions = build_plots(garden)



    if DO_EXAMPLE:
        for reg, body in regions.items():
            print("\n\n")
            
            # sides = {loc: 4 - len(plots[loc]["plot_neighbors"]) for loc in body}
            
            sides = [f"{loc}, {4 - len(plots[loc]["plot_neighbors"])}" for loc in body]
            perimeter = sum( [4 - len(plots[loc]["plot_neighbors"]) for loc in body] )
            area = len(body)
            print(f"Region".ljust(11)+":", f"{reg}")
            print(f"Area :".rjust(12), f"{area}")
            print(f"Perim :".rjust(12), f"{perimeter}", ", ".join(sorted(sides)) )
            print(f"Price :".rjust(12), f"{area * perimeter}\n")

            draw_region(body, {loc: str(4 - len(plots[loc]["plot_neighbors"])) for loc in body})
            # for loc in body:
            #     print(f"Loc :".rjust(12), f"{loc}")
            #     print(f"Neighbors :".rjust(12), f"{plots[loc]['plot_neighbors']}\n")
                
            _ = input("\nPress enter to continue")
        
        
    prices = {}

    for reg, locs in regions.items():
        prices[reg] = len(locs) * sum( [4 - len(plots[loc]["plot_neighbors"]) for loc in locs] )

    return sum(prices.values())




###############################################################################
# PART B
###############################################################################
def solve_b(garden:dict):
    """for solving Part B"""
    print(f"\n\n{'*' * 60} Part B\n\n")

    plots, regions = build_plots(garden)
    regions = {reg: locs for reg, locs in regions.items() if len(locs) > 1}

    region_sides = {}
    
    for reg, locs in regions.items():
        min_x = min(loc[1] for loc in locs)
        max_x = max(loc[1] for loc in locs)
        min_y = min(loc[0] for loc in locs)
        max_y = max(loc[0] for loc in locs)

        sides = 0
        # count top and bottom sides
        sides += 2 * (max_x - min_x + 1)
        # count left and right sides
        sides += 2 * (max_y - min_y + 1)

        # subtract internal sides
        for loc in locs:
            if loc[1] > min_x and loc[1] < max_x:
                if (loc[0], loc[1]-1) in locs:
                    sides -= 1
            if loc[0] > min_y and loc[0] < max_y:
                if (loc[0]-1, loc[1]) in locs:
                    sides -= 1

        region_sides[reg] = sides

    return sum(region_sides.values())


###############################################################################
# command line interface
###############################################################################
if __name__ == "__main__":
    os.system('cls')
    
    # Collect command line arguments
    arguments = argparse.ArgumentParser()
    arguments.add_argument("-e", "--example", help="Bool Flag: Test code with example input instead of default 'input.txt'.", default=False, action="store_true")
    arguments.add_argument("-ea", "--example_A", help="Bool Flag: Test code with example_a input instead of default 'example.txt'.", default=False, action="store_true")
    arguments.add_argument("-eb", "--example_B", help="Bool Flag: Test code with example_b input instead of default 'example.txt'.", default=False, action="store_true")
    arguments.add_argument("-ec", "--example_C", help="Bool Flag: Test code with example_c input instead of default 'example.txt'.", default=False, action="store_true")


    arguments.add_argument("-s", "--submit", help="Bool Flag: Submit answer to server. (defaults to False).", default=False, action="store_true")
    arguments.add_argument("-b", "--part_b", help="Bool Flag: Choses parts 'A' or 'B' to run. (defaults to 'A').", default=False, action="store_true")
    arguments.add_argument("-r", "--refresh", help="Bool Flag: Refresh/update the readme.md file and exit.", default=False, action="store_true")
    arguments.add_argument("-d", "--discord", help="Bool Flag: Send message to discord channel and exit.", default=False, action="store_true")
    arguments.add_argument("-v", "--verbose", help="Bool Flag: allow in code print statements.", default=False, action="store_true")
    
    args = arguments.parse_args()

    su.print_args(vars(args))

    # Load puzzle parameters
    config = toml.load(Path('.env'))
    
    DO_A, DO_B = not args.part_b, args.part_b
    DO_EXAMPLE = args.example
    VERBOSE = args.verbose
    
    # open puzzle info
    puzzle = su.open_puzzle(config)

    if args.discord:
        su.Discord(puzzle=puzzle, config=config)
        sys.exit()
    
    if args.refresh:
        su.refresh_readme(puzzle)
        sys.exit()

    if args.submit:
        p = "A" if DO_A else "B"
        f_ex = '(From Example)' if DO_EXAMPLE else '(From input)'

        input_p = Path( "input.txt" )
        if args.example: input_p = Path("example.txt") ; DO_EXAMPLE = True
        if args.example_A: input_p = Path("example_a.txt") ; DO_EXAMPLE = True
        if args.example_B: input_p = Path("example_b.txt") ; DO_EXAMPLE = True
        if args.example_C: input_p = Path("example_c.txt") ; DO_EXAMPLE = True
        source_input = data( input_p )
        print("Input File:", input_p.as_posix())
        
        result = solve_a(source_input) if DO_A else solve_b(source_input)

        correct_msg = ""
        match f"{'EXPL' if DO_EXAMPLE else 'REAL'}, {p}":
            case "EXPL, A": correct_answer = puzzle.examples[0].answer_a
            # case "EXPL, B": correct_answer = puzzle.examples[0].answer_b
            case "EXPL, B": correct_answer = '34' # puzzle file is corrupt.
            case "REAL, A": correct_answer = puzzle.answer_a if puzzle.answered_a else "unknown"
            case "REAL, B": correct_answer = puzzle.answer_b if puzzle.answered_b else "unknown"
            case _: correct_answer = "unknown"
        
        compare = correct_answer == str(result)
        correct_msg = f"IS CORRECT!! ({correct_answer})" if compare else f"IS NOT CORRECT ({correct_answer})"

        print( f"Solution ({p}): {result} {correct_msg} {f_ex}" )
        if not DO_EXAMPLE: su.submit_result(puzzle, result, p, config)
