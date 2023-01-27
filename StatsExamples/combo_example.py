import os, time, cProfile, concurrent.futures, json
from pathlib import Path
from typing import List, Dict, Optional

from slippi import *
from slippi.combo import generate_clippi_header
import filters
dolphin_queue = generate_clippi_header()

def combo_from_file(file, connect_code: str) -> ComboComputer:
    """Accept file path and connect code, process combos, and return"""
    replay:ComboComputer = ComboComputer()
    replay.prime_replay(file)
    replay.combo_compute(connect_code)
    for c in replay.combos:
        if(
            c.minimum_length(5) and
            c.did_kill and
            c.minimum_damage(40)):
            
            replay.json_export(c)
    
    return replay.queue


def multi_find_combos(dir_path, connect_code: str):
    with os.scandir(dir_path) as thing:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = {executor.submit(combo_from_file, os.path.join(dir_path, entry.name), connect_code) for entry in thing}

            for future in concurrent.futures.as_completed(futures):
                for result in future.result(timeout=10):
                    print("file processed")
                    dolphin_queue["queue"].append(result)

    with open("py_clip_combos.json", "w") as write_file:
        json.dump(dolphin_queue, write_file, indent=4)

    print("Done")


if __name__ == '__main__':
    replay_dir = Path(input("Please enter the path to your directory of your replay files: "))
    code_input = input("Please enter your connect code (TEST#123): ")

    print("Processing...")
    # with os.scandir(replay_dir) as thing:
    #     for entry in thing:
    #         dolphin_queue["queue"].append(combo_from_file(os.path.join(replay_dir, entry.name), code_input))
    

    multi_find_combos(replay_dir, code_input)

