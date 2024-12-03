###### IMPORTS ###############################################################
import aocd, toml, pickle
from pathlib import Path

###### CONSTANTS #############################################################

_YEAR_ = 2015
_DAY_ = 7

_u = Path(".me.aocd")
_p = Path(f".puzzle-{_YEAR_}-{_DAY_}.aocd")
_c = Path(".env")

def save_cfg(cfg):
    try:
        _c.write_bytes(toml.dumps(cfg).encode("utf-8"))
        return f"SUCCESS: Save Config: {_c}"
    except:
        return f"FAILURE: Save Config: {_c}"

def load_cfg():
    try:
        cfg = toml.loads(_c.read_text(encoding="utf-8"))
    except:
        _token = Path("D:/Advent of Code") / ".env"
        cfg = {
            "aoc": {
                "AoC_SESSION" : toml.loads(_token.read_text(encoding="utf-8"))["user"]["token"]
                }
            }
        
    return cfg

###### SETUP #################################################################

cfg = load_cfg()

try:
    _ME_ = pickle.load(_u.open("rb"))
except:
    _ME_ = aocd.models.User(token=cfg["aoc"]["AoC_SESSION"])

try:
    _PUZZLE_ = pickle.load(_p.open("rb"))
except:
    _PUZZLE_ = aocd.models.Puzzle(_YEAR_, _DAY_, _ME_)

cfg["aoc"]["example_answer"] = _PUZZLE_.examples[0]

# cfg["Part_1"] = {}
# if _PUZZLE_.answered_a:
#     cfg["Part_1"]["ANSWER"] = _PUZZLE_.answer_a
# else:
#     cfg["Part_1"]["ANSWER"] = None

# cfg["Part_2"] = {}
# if _PUZZLE_.answered_b:
#     cfg["Part_2"]["ANSWER"] = _PUZZLE_.answer_b
# else:
#     cfg["Part_2"]["ANSWER"] = None


save_cfg(cfg)



# def refresh_cfg():
    
#     try:
#         cfg = toml.loads(_c.read_text(encoding="utf-8"))
#         return cfg
#     except:
#         cfg = {}
#         cfg["aoc"] = {}
#         cfg["Part_1"] = {}
#         cfg["Part_1"]["example"] = {
#                     "d": 72,
#                     "e": 507,
#                     "f": 492,
#                     "g": 114,
#                     "h": 65412,
#                     "i": 65079,
#                     "x": 123,
#                     "y": 456,
#                     }

#     return cfg