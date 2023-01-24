from slippi import *
from pathlib import Path

file = Path(r"C:\Users\ant_b\Documents\Coding Projects\starcraft calculator\sc2calc\py-slippi\Modern Replays\BADS#412 (Sheik) vs NUT#356 (Falco) on DL - 12-12-22 09.06pm .slp")

replay = Game(file)

print(replay.start.match_id)
print(replay.start.is_ranked)

thing = ComboComputer()
thing.prime_replay(file)

thing.combo_compute("NUT#356")

print(len(thing.combos))

