from typing import List, Dict, Optional, Union
from pathlib import Path

from .util import *
from .game import Game
from .id import ActionState, Stage
from .event import Start, Frame, StateFlags
from .metadata import Metadata

class WavedashData(Base):
    r_input_frame: int
    angle: float
    airdodge_frames: int
    distance_during_lag:float

    def __init__(self, r_input_frame:int=0, angle:float=0.0, airdodge_frames:int=0, start_loc:float=0.0, end_loc:float=0.0):
        self.r_input_frame = r_input_frame
        self.angle = angle
        self.airdodge_frames = airdodge_frames
        self.distance = end_loc - start_loc

    def total_startup(self):
        return self.r_input_frame + self.airdodge_frames

    