from PIL import Image, ImageDraw, ImageFont
import pandas as pd

WEEK_WIDTH = 14
LINE_HEIGHT = 30
LINE_GAP = 7 + LINE_HEIGHT
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

width = WEEK_WIDTH * (df["week"].max() - df["week"].min())
height = LINE_GAP * (len(genres))
# print(width, height)

im = Image.new("RGBA", (width, height), (255, 255, 255, 255))
draw = ImageDraw.Draw(im)

for season in seasons:
    episodes = df[df["season"] == season]
    genre = episodes.iloc[0]["genre"]
    draw.rectangle(
        (
            WEEK_WIDTH * (episodes["week"].min() - df["week"].min()),
            genres.index(genre) * LINE_GAP,
            WEEK_WIDTH * (episodes["week"].max() - df["week"].min()),
            genres.index(genre) * LINE_GAP + LINE_HEIGHT,
        ),
        fill=(0, 192, 192),
    )
    for index, episode in episodes.iterrows():
        draw.rectangle(
            (
                WEEK_WIDTH * (episode["week"] - df["week"].min()),
                genres.index(genre) * LINE_GAP,
                WEEK_WIDTH * (episode["week"] - df["week"].min() + 1) - 1,
                genres.index(genre) * LINE_GAP + LINE_HEIGHT,
            ),
            fill=(0, 128, 128),
        )

for season in seasons:
    beginning = df[df["season"] == season].iloc[0]
    genre = beginning["genre"]
    draw.text(
        (
            WEEK_WIDTH * (beginning["week"] - df["week"].min()),
            genres.index(genre) * LINE_GAP + LINE_HEIGHT // 2,
        ),
        season,
        fill=(255, 255, 255, 255),
        anchor="lm",
        font_size=20,
        stroke_width=2,
        stroke_fill=(0, 0, 0, 128),
    )

im.save("plot.png")
