from slippi import *
import os

path = "./"

replay_list = []

with os.scandir(path) as thing:

    print("Files in '% s':" % path)
    for entry in thing :
        if ".slp" in entry.name:
            replay_list.append(Game(entry))

for replay in replay_list:
    