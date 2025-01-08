from PIL import Image, ImageDraw, ImageFont
import pandas as pd
from datetime import datetime

WEEK_HEIGHT = 5
COL_WIDTH = 120
COL_GAP = 20 + COL_WIDTH
OFFSET_TOP = WEEK_HEIGHT * 26
OFFSET_LEFT = 300
OFFSET_YEAR = 50
OFFSET_VERSION = 175
FONT_SIZE = 20
FONT = ImageFont.truetype(
    "/usr/share/fonts/noto/NotoSans-CondensedMedium.ttf", FONT_SIZE
)

genres = [
    "Vanilla SP",
    "Vanilla MP",
    "Modded SP",
    "Modded MP",
    "Team Competition",
    "Map SP",
    "Map MP",
    "TFC",
    "Terraria",
    "Variety",
    "Creative",
    "Tutorials",
]

df = pd.read_csv("./assets/ethoslab.csv")
df = pd.DataFrame([df.week, df.genre, df.season]).transpose()
df = df[df["season"].notna() & df["genre"].notna()]

seasons = list(df["season"].unique())
# print(df)
# print(seasons)

first_week = df["week"].min()
height = OFFSET_TOP + WEEK_HEIGHT * (df["week"].max() - first_week)
width = OFFSET_LEFT + COL_GAP * (len(genres))
# print(width, height)

im = Image.new("RGBA", (width, height), (255, 255, 255, 255))
draw = ImageDraw.Draw(im)


def y_from_date(date: datetime):
    return round(
        OFFSET_TOP
        + WEEK_HEIGHT * (date.timestamp() / (60 * 60 * 24 * 7) - first_week)
    )


def draw_text(coords, text):
    draw.text(
        coords,
        text,
        fill=(255, 255, 255, 255),
        anchor="mt",
        font=FONT,
        stroke_width=4,
        stroke_fill=(31, 31, 31, 255),
    )


for year in range(2010, 2026):
    for month in ["04", "07", "10", "01"]:
        y = y_from_date(datetime.fromisoformat(f"{year}-{month}-01"))
        draw.line(
            (0, y, width, y),
            fill=(0, 0, 0, 255),
            width=3 if month == "01" else 1,
        )
    draw_text((OFFSET_YEAR, y), f"{year}")

for season in seasons:
    episodes = df[df["season"] == season]
    genre = episodes.iloc[0]["genre"]
    draw.rectangle(
        (
            OFFSET_LEFT + genres.index(genre) * COL_GAP,
            OFFSET_TOP + WEEK_HEIGHT * (episodes["week"].min() - first_week),
            OFFSET_LEFT + genres.index(genre) * COL_GAP + COL_WIDTH,
            OFFSET_TOP + WEEK_HEIGHT * (episodes["week"].max() - first_week),
        ),
        fill=(0, 192, 192),
    )
    for index, episode in episodes.iterrows():
        draw.rectangle(
            (
                OFFSET_LEFT + genres.index(genre) * COL_GAP,
                OFFSET_TOP + WEEK_HEIGHT * (episode["week"] - first_week),
                OFFSET_LEFT + genres.index(genre) * COL_GAP + COL_WIDTH,
                OFFSET_TOP
                + WEEK_HEIGHT * (episode["week"] - first_week + 1)
                - 1,
            ),
            fill=(0, 128, 128),
        )

for season in seasons:
    beginning = df[df["season"] == season].iloc[0]
    genre = beginning["genre"]
    draw_text(
        (
            OFFSET_LEFT + genres.index(genre) * COL_GAP + COL_WIDTH // 2,
            OFFSET_TOP + WEEK_HEIGHT * (beginning["week"] - first_week),
        ),
        season,
    )

versions = pd.read_csv("./assets/minecraft-versions.csv")
for index, version in versions.iterrows():
    y = y_from_date(datetime.strptime(version["date"], "%Y-%m-%d"))
    draw_text((OFFSET_VERSION, y), version["name"])

for index, genre in enumerate(genres):
    draw_text((OFFSET_LEFT + index * COL_GAP + COL_WIDTH // 2, 40), genre)

im.save("plot.png")
