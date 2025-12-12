from pathlib import Path
import toml

root_dir = Path(__file__)
while root_dir.name != "Advent-of-Code":
    root_dir = root_dir.parent

root_env = root_dir / ".env"

for dist_env in root_dir.glob("**/.env"):
    if dist_env.resolve() != root_env.resolve():
        print(f"Removing token from {dist_env}")
        _temp = toml.loads(dist_env.read_text(encoding="UTF-8"))
        _temp['user']['token'] = ""
        dist_env.write_text(toml.dumps(_temp), encoding="UTF-8")
print("All done!")