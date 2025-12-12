from aocd.models import Puzzle
from datetime import datetime
from pathlib import Path


def update_header(puzzle: Puzzle):
    """
    Updates the header of the solve file with the date the puzzle was solved
    for parts A and B. If the puzzle has not been solved yet, it leaves the
    header unchanged.

    Parameters:
        puzzle (aocd.models.Puzzle): The AoC puzzle object

    Returns:
        None
    """
    solve_file = Path(f"Solve_{puzzle.year:04}_{puzzle.day:02}.py")

    if solve_file.exists():
        text = solve_file.read_text().split("\n")

    day_done = datetime(
        year=puzzle.year, month=12, day=puzzle.day, hour=0, minute=0, second=0
    )

    text[9] = "# A SOLVED:   N/A".ljust(40) + "#".rjust(40)
    text[10] = "# B SOLVED:   N/A".ljust(40) + "#".rjust(40)

    if puzzle.answered_a:
        dt = day_done + puzzle.my_stats["a"]["time"]
        done = dt.strftime("%Y-%m-%d %H:%M")
        text[9] = f"# A SOLVED:   {done}".ljust(40) + "#".rjust(40)

    if puzzle.answered_b:
        dt = day_done + puzzle.my_stats["b"]["time"]
        done = dt.strftime("%Y-%m-%d %H:%M")
        text[10] = f"# B SOLVED:   {done}".ljust(40) + "#".rjust(40)

    solve_file.write_text("\n".join(text), encoding="utf-8")
