from typing import List
import io, struct
import numpy as np
from pathlib import Path    
import ubjson as ub

# 0x71, 0xe2, 0x1e, 0x0
# 0, 30, 226, 113
file = Path(r"Modern Replays/ACID#441 (Peach) vs NUT#356 (Marth) on FD - 12-15-22 01.42am .slp")


def unpack(fmt, stream):
    fmt = '>' + fmt
    size = struct.calcsize(fmt)
    bytes = stream.read(size)
    if not bytes:
        raise EOFError()
    return struct.unpack(fmt, bytes)

def p_p():
    with open(file, 'rb') as f:
        for i in range(2024306):
            sbubby = unpack("B", f)

def u_p():
    with open(file, 'rb') as f:

        for i in range(2024306):
            byte = f.read(1)
            freef = struct.unpack(">B", byte)


for i in range(50):
    u_p()
    p_p()



