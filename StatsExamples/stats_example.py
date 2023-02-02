from pathlib import Path
import timeit
import os, concurrent.futures, datetime

import polars as pl
from slippi import *

# c_code = "NUT#356"
# file = Path(r"Modern Replays/ACTI#799 (Falcon) vs NUT#356 (Falco) on FoD - 12-15-22 02.06am .slp")
# replay = Game(file)
# stats = StatsComputer()
# stats.prime_replay(replay)
# stats.stats_compute("NUT#356")

def get_wavedash_data(replay, connect_code) -> dict:
    stats = StatsComputer()
    stats.prime_replay(replay)
    stats.wavedash_compute(connect_code)

    player_port, opponent_port = stats.generate_player_ports(connect_code)
    player_port = player_port[0]
    
    formatted_date = stats.metadata.date.replace(tzinfo=None)
    # total number of frames, starting when the player has control, in seconds
    formatted_time = datetime.timedelta(seconds=((stats.metadata.duration - 84)/60)) 
    
    header = {
            "match_id" : stats.rules.match_id,
            "date_time" : formatted_date,
            "duration" : formatted_time,
            "ranked" : stats.rules.is_ranked,
            "win" : stats.is_winner(player_port),
            "char" : id.InGameCharacter(list(stats.players[player_port].characters.keys())[0]).name, #lmao
            "opnt_Char" : id.InGameCharacter(list(stats.players[opponent_port].characters.keys())[0]).name
            }
    wd_data = []
    for wavedash in stats.data.wavedash:
        wd_data.append(header | wavedash.__dict__)
        try:
            wd_data[-1]["direction"] = wd_data[-1]["direction"].name
        except KeyError:
            wd_data[-1]["direction"] = "UNKNOWN"
        
    return wd_data


def stats_from_file(file, connect_code: str) -> pl.DataFrame:
    """Accept file path and connect code, process combos, and return"""
    print(file)
    data_frame = pl.DataFrame(get_wavedash_data(file, connect_code))
    try: 
        data_frame.sort("date_time")
    except:
        data_frame = None
    return data_frame


def multi_find_stats(dir_path, connect_code: str):
    dfs = None
    ind = 0
    with os.scandir(dir_path) as thing:
    #     for entry in thing:
    #         df = stats_from_file(os.path.join(dir_path, entry.name), connect_code)
    #         print("file processed")
    #         if df is not None:
    #             doodad = pl.read_parquet("wavedashdata.parquet")
    #             doodad = pl.concat([doodad, df], how='vertical')
    #             print(doodad)
    #             doodad.write_parquet("wavedashdata.parquet")
    #             print("file written")
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = {executor.submit(stats_from_file, os.path.join(dir_path, entry.name), connect_code) for number, entry in enumerate(thing)}
            
            for future in concurrent.futures.as_completed(futures):
                print(f"processed {ind}")
                ind +=1
                if future.result() is not None:
                    if dfs is None:
                        dfs = future.result()
                        print("creating initial")
                    else:
                        dfs = pl.concat([dfs, future.result()], how='vertical')
                        print("concatting")
                    dfs.write_parquet("wavedashdata_temp.parquet")
                    print("file written")

    # print("start concat")
    # doodad = pl.concat(dfs, how='vertical')
    # print("start write")
    # doodad.write_parquet("wavedashdata_temp.parquet")
    print("Done")



if __name__ == '__main__':
    replay_dir = Path(input("Please enter the path to your directory of your replay files: "))
    code_input = input("Please enter your connect code (TEST#123): ")

    replay_dir = Path(r"C:\Users\ant_b\Documents\Coding Projects\starcraft calculator\sc2calc\py-slippi\Modern Replays")
    code_input = "NUT#356"
    
    print("Processing...")
    multi_find_stats(replay_dir, code_input)