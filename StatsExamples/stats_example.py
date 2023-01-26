from slippi import *
from pathlib import Path

from filters import *

file = Path(r"Modern Replays/BADS#412 (Sheik) vs NUT#356 (Falco) on DL - 12-12-22 09.06pm .slp")

replay = Game(file)

print(replay.start.match_id)
print(replay.start.is_ranked)

thing = StatsComputer()
thing.prime_replay(file)

thing.dash_compute("NUT#356")

# print(len(thing.dashes))

# eef = [dash for dash in thing.dashes if dash.direction == event.Direction.RIGHT]
freef = [dash for dash in thing.dashes if dash.direction == event.Direction.LEFT]
# sbubby = [dash for dash in thing.dashes if dash.is_dashdance]

# print(f"Right: {len(eef)}\nLeft: {len(freef)}\nDashdances: {len(sbubby)}")

# thing.tech_compute("NUT#356")

# print(len(thing.techs))

filtered = filter_direction(thing.dashes, event.Direction.LEFT)

print(len(filtered))
print(len(freef))