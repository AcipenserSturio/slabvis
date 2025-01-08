from PIL import Image, ImageDraw, ImageFont
import pandas as pd
from datetime import datetime

WEEK_HEIGHT = 7
COL_WIDTH = 120
COL_GAP = 20 + COL_WIDTH
FONT_SIZE = 20
FONT = ImageFont.truetype(
    "/usr/share/fonts/noto/NotoSans-CondensedMedium.ttf", FONT_SIZE
)

genres = [
    "Vanilla SP",
    "Vanilla MP",
    "Modded SP",
    "Modded MP",
    "Teamed Competition",
    "Map SP",
    "Map Collab",
    "TFC",
    "Variety",
    "Variety (Terraria)",
    "Creative",
    "Tutorials",
]

df = pd.read_csv("./assets/ethoslab.csv")
df = pd.DataFrame([df.week, df.genre, df.season]).transpose()
df = df[df["season"].notna() & df["genre"].notna()]

seasons = list(df["season"].unique())
# print(df)
# print(seasons)

height = WEEK_HEIGHT * (df["week"].max() - df["week"].min())
width = COL_GAP * (len(genres))
# print(width, height)

im = Image.new("RGBA", (width, height), (255, 255, 255, 255))
draw = ImageDraw.Draw(im)


def y_from_date(date: datetime):
    return round(
        WEEK_HEIGHT * (date.timestamp() / (60 * 60 * 24 * 7) - df["week"].min())
    )


for year in range(2010, 2026):
    for month in ["01", "04", "07", "10"]:
        y = y_from_date(datetime.fromisoformat(f"{year}-{month}-01"))
        draw.line(
            (0, y, width, y),
            fill=(0, 0, 0, 255),
            width=3 if month == "01" else 1,
        )

for season in seasons:
    episodes = df[df["season"] == season]
    genre = episodes.iloc[0]["genre"]
    draw.rectangle(
        (
            genres.index(genre) * COL_GAP,
            WEEK_HEIGHT * (episodes["week"].min() - df["week"].min()),
            genres.index(genre) * COL_GAP + COL_WIDTH,
            WEEK_HEIGHT * (episodes["week"].max() - df["week"].min()),
        ),
        fill=(0, 192, 192),
    )
    for index, episode in episodes.iterrows():
        draw.rectangle(
            (
                genres.index(genre) * COL_GAP,
                WEEK_HEIGHT * (episode["week"] - df["week"].min()),
                genres.index(genre) * COL_GAP + COL_WIDTH,
                WEEK_HEIGHT * (episode["week"] - df["week"].min() + 1) - 1,
            ),
            fill=(0, 128, 128),
        )

for season in seasons:
    beginning = df[df["season"] == season].iloc[0]
    genre = beginning["genre"]
    draw.text(
        (
            genres.index(genre) * COL_GAP + COL_WIDTH // 2,
            WEEK_HEIGHT * (beginning["week"] - df["week"].min()),
        ),
        season,
        fill=(255, 255, 255, 255),
        anchor="mt",
        font=FONT,
        stroke_width=4,
        stroke_fill=(0, 0, 0, 255),
    )

im.save("plot.png")
