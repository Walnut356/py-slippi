from typing import List
import timeit
import io, struct
import numpy as np
from pathlib import Path    
import ubjson as ub
import polars as pl
import pyarrow as pa

from slippi import *
from slippi.event import Start
# 0x71, 0xe2, 0x1e, 0x0
# 0, 30, 226, 113
file = Path(r"Modern Replays/ACID#441 (Peach) vs NUT#356 (Marth) on FD - 12-15-22 01.42am .slp")

print(sum(timeit.repeat("Game(file)", globals=globals(), number=1, repeat=10))/10)
