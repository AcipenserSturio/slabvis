import os
from yt_dlp import YoutubeDL

# Playlist URL and destination file for IDs
URL = "https://www.youtube.com/@xisumavoid"
DEST = "assets/ids.txt"


# Progress hook to process each playlist entry
class StopFetching(Exception):
    pass


def filter_break_on_existing_id(info, *, incomplete):
    if info.get("id") in existing_ids:
        raise StopFetching


with open(DEST) as f:
    existing_ids = set(f.read().strip().split("\n"))


# Main function
def get_playlist():
    with YoutubeDL({"playlist_items": "0"}) as ydl_channel:
        info = ydl_channel.extract_info(URL, download=False)

    # yes, the channel id and the playlist id differ
    # in the first three characters. :shrug:
    url = f"https://www.youtube.com/playlist?list=UUU{info['channel_id'][3:]}"

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


get_playlist()
