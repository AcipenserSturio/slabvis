import pandas as pd
from pathlib import Path
import json
from datetime import datetime

DIR = Path("assets/ethoslab/")
OUT = Path("assets/ethoslab.csv")

COLS = [
    "id",
    "title",
    "duration",
    "view_count",
    "like_count",
    "comment_count",
    "timestamp",
    "upload_date",
    "resolution",
]


def get_metadata():
    for path in DIR.glob("*.info.json"):
        # so the yt-dlp script actually captures
        # the channel object alongside the video objects,
        # which has a 24-char string id
        if len(path.name) != 21:  # id length + ".info.json"
            print(path.name, "skipped")
            continue
        with open(path) as f:
            vid = json.load(f)
        yield [vid[col] for col in COLS]


vids = pd.DataFrame([*get_metadata()], columns=COLS)
vids["week"] = vids["timestamp"].apply(
    lambda timestamp: timestamp // (60 * 60 * 24 * 7)
)
vids.to_csv(OUT)
