from slippi import *
import os
from slippi.event import StateFlags

path = "./"

replay_list = []

# with os.scandir(path) as thing:

#     print("Files in '% s':" % path)
#     for entry in thing :
#         if ".slp" in entry.name:
#             replay_list.append(Game(entry))

# for replay in replay_list:
#     pass

replay: ComboComputer = ComboComputer.prime_replay("Walnut356/py-slippi/Modern Replays/ACTI#799 (Falcon) vs NUT#356 (Falco) on DL - 12-15-22 02.04am .slp")

replay.combo_compute("NUT#356")

print(replay.combos)