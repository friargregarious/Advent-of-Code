__puzzle_year__, __puzzle_day__ = "{year}", "{day}"


def solve_me(part: str, answer=None):
    if answer is not None:
        pass


def version_increment(file_to_increment: str, big: int = 0, med: int = 0, sml: int = 0):
    """increments the version of the file requested"""
    # file_to_increment = f"Solve{__puzzle_year__}_{__puzzle_day__}{file}.py"
    file_text = open(file_to_increment, encoding="utf-8").read().splitlines()

    new_text = []

    for line in file_text:
        if line.startswith("__version__"):
            new_line, old_version = line.split(" = ")
            o_big, o_med, o_sml = [int(x) for x in old_version.strip().split(".")]
            n_big = o_big + big
            n_med = o_med + med
            n_sml = o_sml + sml
            new_vers = f" = {n_big}.{n_med}.{n_sml}"
            new_text.append(new_line + new_vers)
        else:
            new_text.append(line)

    open(file_to_increment, "w", encoding="utf-8").write("\n".join(new_text))
