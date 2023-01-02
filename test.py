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

replay = Game("F:\Coding and Programming\My Projects\VSC\py-slippi\Modern Replays\ACID#441 (Peach) vs NUT#356 (Falco) on FoD - 12-15-22 01.39am .slp")

all_frames = replay.frames

for frame in all_frames:
    if StateFlags.HIT_STUN in frame.ports[0].leader.post.flags:
        print(frame.index)
        print(frame.ports[0].leader.post.flags.HIT_STUN)