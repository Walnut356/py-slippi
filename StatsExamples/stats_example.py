from pathlib import Path
from math import isclose

from slippi import *

file = Path(r"Modern Replays/ACTI#799 (Falcon) vs NUT#356 (Falco) on FoD - 12-15-22 02.06am .slp")

replay = Game(file)

print(replay.start.match_id)
print(replay.start.is_ranked)

thing = StatsComputer()
thing.prime_replay(file)

thing.sdi_compute()

print(len(thing.sdis))

dist = [sdi for sdi in thing.sdis if not isclose(sdi.distance(), 0, rel_tol=.01)]

starend = [sdi for sdi in thing.sdis if sdi.start_position != sdi.end_position]

print(dist == starend)
