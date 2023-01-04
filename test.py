from slippi import *
import os
from slippi.combo import ComboComputer
from slippi.event import StateFlags
from pathlib import Path

path: os.PathLike = "C:\\Users\\ant_b\\Documents\\Coding Projects\\starcraft calculator\\sc2calc\\py-slippi\\Modern Replays\\"

replay_list = []

with os.scandir(path) as thing:

    for entry in thing :
        if ".slp" in entry.name:
            print(entry.name)
            replay:ComboComputer = ComboComputer()
            os.close(thing)
            replay.prime_replay(path)
            replay.combo_compute("NUT#356")

            print(len(replay.combos))
            for c in replay.combos:
                if(len(c.moves) >=5 and
                   c.end_percent - c.start_percent > 30):
                    print(c.start_frame)
    