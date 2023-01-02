from slippi import *
import os
from slippi.combo import ComboComputer
from slippi.event import StateFlags

path: os.PathLike = "/workspaces/py-slippi/Modern Replays/Game_20221227T202334.slp"

replay_list = []

# with os.scandir(path) as thing:

#     print("Files in '% s':" % path)
#     for entry in thing :
#         if ".slp" in entry.name:
#             replay_list.append(Game(entry))

# for replay in replay_list:
#     pass

replay: ComboComputer = ComboComputer()

replay.prime_replay(path)
replay.combo_compute("NUT#356")

print(replay.combos)

for c in replay.combos:

    print(c.player)
    print(len(c.moves))
    print(c.did_kill)
    print(c.start_frame)
    print(c.end_frame)
    print(c.start_percent)
    print(c.end_percent)
