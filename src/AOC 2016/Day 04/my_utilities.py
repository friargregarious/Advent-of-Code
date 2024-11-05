import pickle
import toml
from pathlib import Path

########## Loading Configuration
cfg = toml.loads(Path(".env").read_text(encoding="utf-8"))

########## Saving and Loading puzzle files
def pickle_me(title, data):
    """Saves the data with title as filename"""
    Path(title).write_bytes(pickle.dumps(data))

    # with open(title, "wb") as pikd:
    #     pickle.dump(data, pikd)


def unpickle_me(file):
    """loads and returns a pickled objects"""
    return pickle.loads(Path(file).read_bytes())

    # with open(file, "rb") as pikd:
    #     data = pickle.load(pikd)
    # return data

########## Solving Puzzles
def solve_me(part: str, answer=None):
    if part.lower() == "a":
        solve_a(answer)
    elif part.lower() == "b":
        solve_b(answer)
    else:
        print("Could not solve puzzle.")
        

def solve_a(answer=None):
    if answer is not None:
        pfile = Path(cfg["puzzle"]["pfname"])
        puzzle = unpickle_me(pfile)
        puzzle.answer_a = answer
    else:
        print("Did not submint an answer for 'a'.")


def solve_b(answer=None):
    if answer is not None:
        pfile = Path(cfg["puzzle"]["pfname"])
        puzzle = unpickle_me(pfile)
        puzzle.answer_b = answer
    else:
        print("Did not submint an answer for 'b'.")


########## Increment Version and Build Numbers
def version_increment(file_to_increment: str, big: int = 0, med: int = 0, sml: int = 0):
    """increments the version of the file requested"""
    # file_to_increment = f"Solve{__puzzle_year__}_{__puzzle_day__}{file}.py"
    file_text = Path(file_to_increment).read_text(encoding="utf-8").splitlines()

    new_text = []

    for line in file_text:
        if line.startswith("__version__"):
            new_line, old_version = line.split(" = ")
            old_version = old_version.strip(' " ')
            o_big, o_med, o_sml = [int(x) for x in old_version.split(".")]

            n_big = o_big + big
            n_med = o_med + med
            n_sml = o_sml + sml

            vs = ".".join(map(str, [n_big, n_med, n_sml]))
            vstr = f'{new_line} = "{vs}" ' 
            new_text.append(vstr)
            
        elif line.startswith("__build__"):
            new_line, old_build = line.split(" = ")
            new_build = int(old_build) + sum([big, med, sml])
            new_text.append(f"{new_line} = {new_build}")            
        else:
            new_text.append(line)

    Path(file_to_increment).write_text("\n".join(new_text), encoding="utf-8")
