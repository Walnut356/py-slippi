from pathlib import Path
from math import isclose
import timeit
import os, concurrent.futures, datetime

import pandas as pd
import pyarrow.parquet as parquet
from slippi import *

file = Path(r"Modern Replays/ACTI#799 (Falcon) vs NUT#356 (Falco) on FoD - 12-15-22 02.06am .slp")

replay = Game(file)
stats = StatsComputer()
stats.prime_replay(replay)
stats.stats_compute("NUT#356")

wd_data = {"DateTime" : str(stats.metadata.date.date()) + " " + str(stats.metadata.date.time()),
           "Duration" : stats.metadata.duration,
           "Duration" : stats.metadata.duration,
           "Ranked" : stats.rules.is_ranked,
           "Char" : id.InGameCharacter(list(stats.players[stats.generate_player_ports("NUT#356")[0][0]].characters.keys())[0]).name,
           "Angle" : [],
           "Direction" : []}

for wavedash in stats.data.wavedash:

    wd_data["Angle"].append(wavedash.angle)
    wd_data["Direction"].append(wavedash.direction.name)


df = pd.DataFrame(wd_data)

#df = df.set_index([df.index, "DateTime"])




file = Path(r"Modern Replays\DAT#645 (Fox) vs NUT#356 (Falco) on YS - 12-12-22 07.15pm .slp")

replay = Game(file)
stats = StatsComputer()
stats.prime_replay(replay)
stats.stats_compute("NUT#356")

wd_data = {"DateTime" : str(stats.metadata.date.date()) + " " + str(stats.metadata.date.time),
           "Duration" : stats.metadata.duration,
           "Ranked" : stats.rules.is_ranked,
           "Char" : id.InGameCharacter(list(stats.players[stats.generate_player_ports("NUT#356")[0][0]].characters.keys())[0]).name,
           "Angle" : [],
           "Direction" : []}

for wavedash in stats.data.wavedash:

    wd_data["Angle"].append(wavedash.angle)
    wd_data["Direction"].append(wavedash.direction.name)


df2 = pd.DataFrame(wd_data)

#df2 = df2.set_index([df.index, "DateTime"])

df = df.merge(df2, how="outer")

df.to_excel("wavedashdata.xlsx", sheet_name="Sheet1")






# def stats_from_file(file, connect_code: str) -> StatsComputer():
#     """Accept file path and connect code, process combos, and return"""
#     replay:StatsComputer = StatsComputer()
#     replay.prime_replay(file)
#     replay.stats_compute(connect_code)
    
#     return replay.data


# def multi_find_stats(dir_path, connect_code: str):
#     with os.scandir(dir_path) as thing:
#         with concurrent.futures.ProcessPoolExecutor() as executor:
#             futures = {executor.submit(stats_from_file, os.path.join(dir_path, entry.name), connect_code) for entry in thing}

#             for future in concurrent.futures.as_completed(futures):
#                 for result in future.result(timeout=10):
#                     print("file processed")
#                     dolphin_queue["queue"].append(result)

#     with open("py_clip_combos.json", "w") as write_file:
#         json.dump(dolphin_queue, write_file, indent=4)

#     print("Done")


# if __name__ == '__main__':
#     replay_dir = Path(input("Please enter the path to your directory of your replay files: "))
#     code_input = input("Please enter your connect code (TEST#123): ")

#     print("Processing...")

#     multi_find_combos(replay_dir, code_input)