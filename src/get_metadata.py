import yt_dlp
import json
import pandas as pd
from pathlib import Path
import csv

# roughly equivalent to:
# yt-dlp --skip-download --write-info-json --output "${out}/%(id)s.%(ext)s" -a ${queue}

LIMIT = 100
COLS = [
    "id",
    "title",
    "uploader_id",
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


def get_metadata(queue, sheet):
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
    with yt_dlp.YoutubeDL({"cookiefile": "cookies.txt"}) as ydl:
        for id_ in ids[:LIMIT]:
            try:
                result = ydl.extract_info(id_, download=False)
            except yt_dlp.DownloadError:
                # if any video goes unavailable before the downloader
                # gets it, it will keep being attempted every run.
                # redo better? move to the end of the queue?
                continue
            # print(result)
            row = [result[col] if col in result else None for col in COLS]
            row[COLS.index("week")] = row[COLS.index("timestamp")] // 604800
            with open(sheet, "a") as f:
                csv.writer(f).writerow(row)

            # with open(f"assets/{id_}.info.json", "w") as f:
            #     json.dump(result, f, indent="  ")

    pd.read_csv(sheet).sort_values("timestamp").to_csv(sheet, index=False)


queue = "assets/queue.txt"
sheet = "assets/metadata.csv"

get_metadata(queue, sheet)
