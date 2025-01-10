import yt_dlp
import json
from pathlib import Path


def get_playlist(url, dest):
    # equivalent to:
    # rm ${dest}
    # yt-dlp --flat-playlist -i --print-to-file id ${dest} ${url}

    with open(dest, "w") as f:
        f.write("")

    ydl_opts = {
        "print_to_file": {"video": [("%(id)s", dest)]},
        "extract_flat": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(url)


# URL = "https://www.youtube.com/playlist?list=PL96C35uN7xGLDEnHuhD7CTZES3KXFnwm0"
# DEST = "assets/tomscott.txt"


URL = "https://www.youtube.com/@xisumavoid"
DEST = "assets/xisuma.txt"

get_playlist(URL, DEST)
