import yt_dlp
import json
import pandas as pd
from pathlib import Path
import csv

# roughly equivalent to:
# yt-dlp --skip-download --write-info-json --output "${out}/%(id)s.%(ext)s" -a ${queue}

LIMIT = 10
COLS = [
    "id",
    "title",
    "duration_string",
    "resolution",
    "view_count",
    "like_count",
    "comment_count",
    "timestamp",
    "upload_date",
    "epoch",
    "week",
    "genre",
    "series",
]


def get_metadata(queue, sheet, out):
    with open(queue) as f:
        ids = f.read().strip().split("\n")

    if Path(sheet).exists():
        df = pd.read_csv(sheet)
    else:
        df = pd.DataFrame([], columns=COLS)
        df.to_csv(sheet, index=False)

    cached = set(df["id"])
    ids = [id_ for id_ in ids if id_ not in cached]

    # Run yt-dlp
    with yt_dlp.YoutubeDL({"cookies": ["cookies.txt"]}) as ydl:
        for id_ in ids[:LIMIT]:
            result = ydl.extract_info(id_, download=False)
            row = [result[col] if col in result else None for col in COLS]
            row[COLS.index("week")] = row[COLS.index("timestamp")] // 604800
            with open(sheet, "a") as f:
                csv.writer(f).writerow(row)

    pd.read_csv(sheet).sort_values("timestamp").to_csv(sheet, index=False)

    # with open(f"{out}/{id_}.info.json", "w") as f:
    #     json.dump(result, f, indent="  ")


queue = "assets/xisuma.txt"
sheet = "assets/xisumavoid.csv"
out = "assets/xisuma"

get_metadata(queue, sheet, out)
