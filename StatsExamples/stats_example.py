from pathlib import Path
from math import isclose
import timeit
import os, concurrent.futures, datetime

import polars as pl
from slippi import *

c_code = "NUT#356"

file = Path(r"Modern Replays/ACTI#799 (Falcon) vs NUT#356 (Falco) on FoD - 12-15-22 02.06am .slp")
replay = Game(file)
# stats = StatsComputer()
# stats.prime_replay(replay)
# stats.stats_compute("NUT#356")

def get_data(replay, connect_code) -> dict: 
    stats = StatsComputer()
    stats.prime_replay(replay)
    stats.stats_compute(connect_code)

    player_port, opponent_port = stats.generate_player_ports(connect_code)
    player_port = player_port[0]
    formatted_date = stats.metadata.date.replace(tzinfo=None)
    formatted_time = datetime.timedelta(seconds=(stats.metadata.duration/60))
    #HACK there's literally not a better way to do this. replace() method doesn't exist for timedelta, and if you don't want a string as the output
    #all you can do is reconstruct the object.
    formatted_time = datetime.timedelta(seconds=formatted_time.seconds, microseconds=round(formatted_time.microseconds, 0))
    
    header = {"DateTime" : formatted_date,
            "Duration" : formatted_time,
            "Ranked" : stats.rules.is_ranked,
            "Win" : stats.is_winner(player_port),
            "Char" : id.InGameCharacter(list(stats.players[player_port].characters.keys())[0]).name, #lmao
            "Opnt Char" : id.InGameCharacter(list(stats.players[opponent_port].characters.keys())[0]).name
            }
    wd_data = []
    for wavedash in stats.data.wavedash:
        wd_data.append(header | wavedash.__dict__)
        wd_data[-1]["direction"] = wd_data[-1]["direction"].name
        
    
    return wd_data


df = pl.DataFrame(get_data(replay, c_code)).lazy()


file = Path(r"Modern Replays/DAT#645 (Fox) vs NUT#356 (Falco) on YS - 12-12-22 07.15pm .slp")

replay = Game(file)

df2 = pl.DataFrame(get_data(replay, c_code)).lazy()

df = df.sort("DateTime")
df2 = df2.sort("DateTime")

thing = df.merge_sorted(df2, "DateTime").collect()

thing.write_parquet("wavedashdata.parquet")






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