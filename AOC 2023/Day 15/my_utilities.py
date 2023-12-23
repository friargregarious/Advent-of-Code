import bz2, pickle
import configparser

__puzzle_year__, __puzzle_day__ = "2023", "15"


def path(*args) -> str:
    """cleans up escaped characters and will put 2"""
    for item in args:
        item = item.strip()  # get rid of whitespaces and unprintables

        while chr(92) in item:
            # get rid of all escaped chars
            item = item.replace(chr(92), "/")

        while "//" in item:
            # sometimes we end up with double seperators within path string
            # but we still want to keep at least one.
            item = item.replace("//", "/")

        # we don't want any extra separators at the ends of the paths
        item = item.strip("/")

    return "/".join(args)


def loosen(file):
    """loads and returns a pickled objects"""
    # with open(file, 'rb') as pikd:
    # data = pickle.load(pikd)
    # if file.endswith(".aocd"):
    data = bz2.BZ2File(file, "rb")
    data = pickle.load(data)
    return data
    # raise TypeError


def solve_a(answer=None):
    if answer is not None:
        cfg = configparser.ConfigParser()
        cfg.read(".env")
        # pfname =
        pfile = path(cfg.get("puzzle", "pfname"))

        puzzle = loosen(pfile)
        print(
            f"Loaded {pfile}\nSubmiting {answer} for part 'A'\n... waiting for response."
        )
        puzzle.answer_a = answer
    else:
        print("Did not submint an answer")


def solve_b(answer=None):
    if answer is not None:
        cfg = configparser.ConfigParser()
        cfg.read(".env")
        # pfname =
        pfile = path(cfg.get("puzzle", "pfname"))

        puzzle = loosen(pfile)
        print(
            f"Loaded {pfile}\nSubmiting {answer} for part 'B'\n... waiting for response."
        )
        puzzle.answer_b = answer
    else:
        print("Did not submint an answer")


def version_increment(file_to_increment: str, big: int = 0, med: int = 0, sml: int = 0):
    """increments the version of the file requested"""
    # file_to_increment = f"Solve{__puzzle_year__}_{__puzzle_day__}{file}.py"
    file_text = open(file_to_increment, encoding="utf-8").read().splitlines()

    new_text = []

    for line in file_text:
        if line.startswith("__version__"):
            new_line, old_version = line.split(" = ")
            old_version = old_version.strip('"')
            o_big, o_med, o_sml = [int(x) for x in old_version.split(".")]
            n_big = o_big + big
            n_med = o_med + med
            n_sml = o_sml + sml
            new_vers = f' = "{n_big}.{n_med}.{n_sml}"'
            new_text.append(new_line + new_vers)
        else:
            new_text.append(line)

    open(file_to_increment, "w", encoding="utf-8").write("\n".join(new_text))
