import os
from yt_dlp import YoutubeDL


# Progress hook to process each playlist entry
class StopFetching(Exception):
    pass


def filter_break_on_existing_id(info, *, incomplete):
    if info.get("id") in existing_ids:
        raise StopFetching


# Main function
def get_playlist(url):
    with YoutubeDL({"playlist_items": "0"}) as ydl_channel:
        info = ydl_channel.extract_info(url, download=False)

    # yes, the channel id and the playlist id differ
    # in the first two characters. :shrug:
    url = f"https://www.youtube.com/playlist?list=UU{info["channel_id"][2:]}"

    ydl_opts = {
        "extract_flat": True,
        "lazy_playlist": True,
        "print_to_file": {"video": [("%(id)s", DEST)]},
        "match_filter": filter_break_on_existing_id,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=False)
    except StopFetching:
        print("Stopped fetching: Existing ID encountered.")


CHANNELS = "assets/channels.txt"
DEST = "assets/queue.txt"

with open(DEST) as f:
    existing_ids = set(f.read().strip().split("\n"))

with open(CHANNELS) as f:
    urls = f.read().strip().split("\n")

for url in urls:
    get_playlist(url)
