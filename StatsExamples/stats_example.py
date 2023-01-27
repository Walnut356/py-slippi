from pathlib import Path

from slippi import *

file = Path(r"Modern Replays/BADS#412 (Sheik) vs NUT#356 (Falco) on DL - 12-12-22 09.06pm .slp")

replay = Game(file)

print(replay.start.match_id)
print(replay.start.is_ranked)

thing = StatsComputer()
thing.prime_replay(file)

thing.dash_compute("NUT#356")

print(len(thing.dash_compute("NUT#356")))

