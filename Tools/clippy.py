from pathlib import Path
from uuid import uuid4

root_dir = Path(__file__)
while root_dir.name != "Advent-of-Code":
    root_dir = root_dir.parent

clip_dir = root_dir / ".junk"
if not clip_dir.exists(): clip_dir.mkdir()

files_to_cull = ["**/clip*", "**/*junk*.py"]


for pattern in files_to_cull:
    clip_list = root_dir.glob(pattern)
    
    for clip_path in clip_list:
        target_path = clip_dir / f"{uuid4().hex}_{clip_path.name}"
        if ".junk" not in clip_path.resolve().parts[:-1] and clip_path.name != "clippy.py":
            target_path.write_text(clip_path.read_text(encoding="UTF-8"), encoding="UTF-8")

            clip_path.unlink()


