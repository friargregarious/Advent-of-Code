from numpy import where
import os, requests, json, toml, argparse
from tracemalloc import start
import matplotlib.pyplot as plt

from pathlib import Path
from datetime import datetime
# from bs4 import BeautifulSoup

cfgpath = Path().cwd().parent / ".env"
cfg = toml.loads(cfgpath.read_text())
cfgpath.write_text(toml.dumps(cfg))

now = datetime.now()
GAME_ON = now.month == 12 and 1 <= now.day <= 25
GAME_OVER = now.month == 12 and now.day > 25

aocd_leaderboard_data = json.loads(Path("leaderboard.json").read_text())

def update_leaderboard(existing:dict):
    members = {}
    
    for key, data in existing["members"].items():
        name = data["name"]
        members[name] = {}
        members[name]["id"] = key
        members[name]["local_score"] = 0
        members[name]["star_count"] = data["stars"]
        members[name]["stars"] = {}
        members[name]["days"] = {}
        
        comp = data["completion_day_level"]

        for day, stars in comp.items():
            for star, stuff in stars.items():
                finish_line = datetime(year=now.year, month=now.month, day=int(day)+1, hour=0, minute=0, second=0).timestamp()
                _age = int(finish_line - float(stuff["get_star_ts"]))
                age = _age if _age > 0 else 0
                members[name]["stars"][f"{day}-{star}"] = age

                members[name]["local_score"] += age
                
                if day in members[name]["days"]:
                    members[name]["days"][day] += age
                else:
                    members[name]["days"][day] = age
                
        #         print(f"{name}, {day}, {star}: {finish_line:,}, {stuff['get_star_ts']:,}, {age:,}")
        #     print(f"Day #{day} Score: {members[name]["days"][day]:,}")
        # print(f"Total Score: {members[name]["local_score"]:,}\n")

    return members

def refresh_leaderboard_data():
    # user_stats = aocd.models.User(token).get_stats(now.year)
    # https://adventofcode.com/2024/leaderboard/private/view/2588518.json
    try:
        new_data = requests.get(cfg["leaderboard"]["address"], cookies={"session" : cfg["user"]["token"]} ).json()
        Path("leaderboard.json").write_text(json.dumps(new_data, indent=3))
        print("Success updating leaderboard data.")
    except:
        print("Error getting leaderboard data.")


def plot_day_scores(data:dict, day:int):
    stats = []
    for k, v in data.items():
        if str(day) in v["days"]:
            stats.append((v["days"][str(day)], k))
        else:
            stats.append((0, k))
    
    scores, names = zip(*sorted(stats, reverse=True))
    
    print(scores, "\n", names)

def plot_star_scores(data:dict):
    pass

def plot_leaderboard(data:dict):

    pass
    # # Plotting
    # plt.bar(json_data["categories"], json_data["values"])
    # plt.xlabel('Categories')
    # plt.ylabel('Values')
    # plt.title('Bar Chart of JSON Data')
    # plt.show()
    



if __name__ == "__main__":
    os.system("cls")
    args = argparse.ArgumentParser()

    args.add_argument("--refresh", help="Refresh the leaderboard data.", type=bool, default=False)
    args.add_argument("--day", type=int)
    args = args.parse_args()
    
    if args.refresh:
        refresh_leaderboard_data()
    
    print("Args:", args.refresh, args.day)

    member_data = update_leaderboard(aocd_leaderboard_data)
    plot_day_scores(member_data, 2)
