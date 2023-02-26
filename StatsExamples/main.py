from pathlib import Path
from slippi import *

replay = Game(Path(r'Modern Replays/Game_20221227T194333.slp'))

frames = []
flags = []
for frame in replay.frames:
    frames.append(frame.ports[0].leader)
    flags.append(frame.ports[0].leader.post.flags)

print("done")