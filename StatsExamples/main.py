from pathlib import Path
from slippi import *
import polars as pl

# replay = Game(Path(r'Modern Replays/Game_20221227T194333.slp'))

# frames = []
# flags = []
# for frame in replay.frames:
#     frames.append(frame.ports[0].leader)
#     flags.append(frame.ports[0].leader.post.flags)

# print("done")

data = pl.read_csv(Path(r"StatsExamples/SSBM Data Sheet (1.02) - Character Attributes.csv"))

thing = data.filter(pl.col("name") == "Falco")

print(thing)
print(thing.get_column("gravity"))