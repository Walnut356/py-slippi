from slippi import *
from pathlib import Path

file = Path(r"E:\Slippi Replays\Netplay\Game_20230116T194232.slp")

replay = Game(file)

print(replay.start.match_id)
print(replay.start.is_ranked)

file = Path(r"E:\Slippi Replays\Netplay\Game_20230119T065241.slp")

replay = Game(file)

print(replay.start.match_id)
print(replay.start.is_ranked)