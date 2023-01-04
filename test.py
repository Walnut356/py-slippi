import os, time, cProfile, concurrent.futures, json
from pathlib import Path
from typing import List, Dict, Optional

from slippi import *
from slippi.combo import ComboComputer

dolphin_queue = {
  "mode": "queue",
  "replay": "",
  "isRealTimeMode": False,
  "outputOverlayFiles": True,
  "queue": [
  ]
}

PRE_COMBO_BUFFER = -60
POST_COMBO_BUFFER = 90

def combo_from_file(file, connect_code: str):
    replay:ComboComputer = ComboComputer()
    replay.prime_replay(file)
    replay.combo_compute(connect_code.upper())
    
    data: List[Dict] = []
    
    for c in replay.combos:
        if(len(c.moves) >=5 and
            c.did_kill and
            c.end_percent - c.start_percent > 40
            ):
            data.append({})
            data[-1]["path"] = file
            data[-1]["gameStartAt"] = replay.metadata.date.strftime("%m/%d/%y %I:%M %p")
            data[-1]["startFrame"] = c.start_frame + PRE_COMBO_BUFFER
            data[-1]["endFrame"] = c.end_frame + POST_COMBO_BUFFER
    return data

def multi_find_combos(path, conn_code: str):
    with os.scandir(replay_dir) as thing:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = {executor.submit(combo_from_file, os.path.join(replay_dir, entry.name), code_input) for entry in thing}
            
            for future in concurrent.futures.as_completed(futures):
                for result in future.result():
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
    
