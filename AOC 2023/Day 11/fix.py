import os

fname = "Solve2023_11a.py"

file_text = open(fname).read()
open(fname + ".bu", "w").write(file_text)

replacements = {
    "my_utils": "my_utilities",
    "\t": "    ",
    "parse(": "parse_input(",
    "Solve_a": "solve_a",
}

for look_for, repl_with in replacements.items():
    file_text = file_text.replace(look_for, repl_with)


open(fname, "w").write(file_text)

black_string = f"""black {fname} --safe -q"""


os.system(black_string)
