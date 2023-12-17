import os
import sys
import time
import bz2
import pickle

# import configparser
from datetime import datetime
import aocd
import json

# from termcolor import colored

# os.system("cls")
# now = datetime.now()
# cfg = configparser.ConfigParser()
# cfg.read(".env")
# token = cfg.get("user", "token")

# for year in range(2015, now.year + 1):
#     user_stats = aocd.models.User(token).get_stats()
# user_stats = aocd.models.User(token).get_stats(years=now.year)
# open("stats.json","w").write(json.dumps(user_stats, indent=True))


class Rankings(dict):
    def __init__(self, user_token):
        self.user = aocd.models.User(user_token)

    def get_day_stats(self, year: int, day: int) -> list:
        y_key = str(year)
        d_key = f"{day:02}"
        # puz_fn = f".puzzles/P{y_key}_{d_key}.aocd"
        puz_fn = f".puzzles/{y_key}-{d_key}.aocd"
        if os.path.isfile(puz_fn):
            try:
                # puzzle = loosen(puz_fn)
                puzzle = unpickle_me(puz_fn)
            except:
                time.sleep(10)
                puzzle = aocd.models.Puzzle(year, day, self.user)
                # compressed_pickle(puz_fn, puzzle)
                pickle_me(puz_fn, puzzle)

        else:
            time.sleep(10)
            puzzle = aocd.models.Puzzle(year, day, self.user)
            # compressed_pickle(puz_fn, puzzle)
            pickle_me(puz_fn, puzzle)

        title = puzzle.title

        if y_key not in self:
            self.pull_from_local(year)
            if y_key not in self:
                self.pull_year_from_aocd(year)
                if y_key not in self:
                    raise KeyError(f"{year} has no completed puzzles.")

        if d_key not in self[y_key]:
            raise KeyError(f"{year}-{day} was not completed.")

        part_data = []
        for part in ["a", "b"]:
            rank, points = [0, 0]
            # part_data.append([part, rank, points])

            if part in self[y_key][d_key]:
                _, rank, points = self[y_key][d_key][part]  # [1:]
                part_data.append([part, rank, points])
            else:
                part_data.append([part, 0, 0])

        return_info = {"title": title, "parts": part_data}

        return return_info

    def save_to_local(self) -> None:
        try:
            jtext = json.dumps(self, indent=3, sort_keys=True)
            open("stats.json", "w").write(jtext)
            return True
        except Exception as e:
            print(e)
            sys.exit(e)

    def pull_from_local(self, year: int = 0):
        grabbed = dict(json.loads(open("stats.json").read()))
        if year > 0:
            YEAR_KEY = str(year)
            if YEAR_KEY not in self:
                self[YEAR_KEY] = grabbed[YEAR_KEY]

            if YEAR_KEY in grabbed:
                self[YEAR_KEY] = grabbed[YEAR_KEY]
                return True
            raise KeyError(f"{year} not found in local.")
        else:
            self.update(grabbed)

    def pull_year_from_aocd(self, year: int) -> None:
        time.sleep(10)
        grabbed = self.user.get_stats(year)

        for date_stamp, stats_body in grabbed.items():
            day = int(date_stamp.split("/")[1])
            # day_key = f"{year}_{int(day):02}"
            if str(year) not in self:
                self[str(year)] = {}

            if f"{day:02}" not in self[str(year)]:
                self[str(year)][f"{day:02}"] = {}

            # print("\n", colored(f"{year}, {day}", "red"))
            for day_part in stats_body:
                time_string = str(stats_body[day_part]["time"])
                # print(colored(time_string, "green"))

                try:
                    hrs, mins, secs = time_string.split(":")
                    this_day_stamp = datetime(
                        int(year),
                        12,
                        int(day),
                        int(hrs),
                        int(mins),
                        int(secs),
                        tzinfo=None,
                    )

                except Exception:
                    this_day_stamp = datetime(int(year), 12, int(day) + 1)

                completed = this_day_stamp.strftime(format="%Y-%m-%d %H:%M:%S")
                rank = stats_body[day_part]["rank"]
                score = stats_body[day_part]["score"]

                data = [completed, rank, score]

                if day_part not in self[str(year)][f"{day:02}"]:
                    self[str(year)][f"{day:02}"][day_part] = data
                else:
                    self[str(year)][f"{day:02}"][day_part].update(data)


def compressed_pickle(title, data):
    """Saves the "data" with the "title" and adds the .pickle"""

    # with open(title + ".aocd", "wb") as pikd:
    #     pickle.dump(data, pikd)
    # if not title.endswith(".aocd"):
    #     title += ".aocd"

    with bz2.BZ2File(title, "w") as f:
        pickle.dump(data, f)


def loosen(file):
    """loads and returns a pickled objects"""
    # with open(file, 'rb') as pikd:
    # data = pickle.load(pikd)
    # if file.endswith(".aocd"):
    data = bz2.BZ2File(file, "rb")
    data = pickle.load(data)
    return data
    # raise TypeError


def pickle_me(title, data):
    """Saves the "data" with the "title" and adds the .pickle"""

    with open(title, "wb") as pikd:
        pickle.dump(data, pikd)


def unpickle_me(file):
    """loads and returns a pickled objects"""
    with open(file, "rb") as pikd:
        data = pickle.load(pikd)
    return data
