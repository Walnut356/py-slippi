from typing import List, Dict, Optional, Union
from pathlib import Path
from math import atan2, degrees

from .util import Base as Base
from .game import Game
from .id import ActionState, Stage
from .event import Start, Frame, StateFlags, Position, Buttons, Direction
from .metadata import Metadata
from .combo import PlayerIndex
from .common import *

class WavedashData(Base):
    r_frame: int # which airborne frame was the airdodge input on?
    angle: float # in degrees
    airdodge_frames: int
    waveland: bool

    def __init__(self, r_input_frame:int=0, angle:Position=None, airdodge_frames:int=0):
        self.r_frame = r_input_frame
        if angle.x and angle.y:
            # atan2 converts coordinates to degrees without losing information (tan quadrent 1 and 3 are both positive)
            self.angle = degrees(atan2(angle.y, angle.x))
            # then we need to normalize the values to degrees-below-horizontal
            #TODO track # of left and right wavedashes, angle by direction, but still output normalized
            self.angle = self.angle + 180 if self.angle < -90 else self.angle + 90
        else:
            self.angle = 0
        self.airdodge_frames = airdodge_frames
        self.waveland = True

    def total_startup(self) -> int:
        return self.r_frame + self.airdodge_frames
    
class DashData(Base):
    start_pos: float
    end_pos: float
    is_dashdance: bool

    def __init__(self, start_pos=0, end_pos = 0):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.is_dashdance = False

    def distance(self) -> float:
        return abs(self.end_pos - self.start_pos)

class TechData(Base):
    tech_type: common.TechType
    tech_direction: Direction
    is_missed_tech: bool
    towards_center: bool
    towards_opponent: bool
    jab_reset: bool

    def __init__(self):
        pass
    


class StatsComputer(Base):
    rules: Optional[Start]
    players: List[PlayerIndex]
    all_frames: List[Frame]
    metadata: Optional[Metadata]
    wavedashes: List[WavedashData]
    dashes: List[DashData]
    
    def __init__(self):
        self.rules = None
        self.players = []
        self.all_frames = []
        self.metadata = None
        self.wavedashes = []
    
    def prime_replay(self, replay_path, retain_data=False) -> None:
        """Parses a replay and loads the relevant data into the combo computer. Call combo_compute(connect_code) to extract combos
        from parsed replay"""
        parsed_replay = Game(replay_path)
        self.rules = parsed_replay.start
        for i in range(0,2):
            self.players.append(PlayerIndex(parsed_replay.start.players[i], parsed_replay.metadata.players[i].connect_code, i))
        self.all_frames = parsed_replay.frames
        self.metadata = parsed_replay.metadata
        self.replay_path = replay_path
        if not retain_data:
            self.wavedashes = []

    def wavedash_compute(self, connect_code: str):
        player_port = None
        for player in self.players:
            if player.code == connect_code.upper():
                player_port = player.port
                break
        
        for i, frame in enumerate(self.all_frames):
            player_frame = frame.ports[player_port].leader
            player_state = player_frame.post.state
            prev_player_frame = port_frame_by_index(player_port, i - 1, self.all_frames)
            
            if player_state == ActionState.LAND_FALL_SPECIAL and prev_player_frame.post.state != ActionState.LAND_FALL_SPECIAL:
                for j in reversed(range(0, 5)):
                    past_frame = port_frame_by_index(player_port, i - j, self.all_frames)
                    if Buttons.Physical.R in past_frame.pre.buttons.physical.pressed() or Buttons.Physical.L in past_frame.pre.buttons.physical.pressed():
                        self.wavedashes.append(WavedashData(0, player_frame.pre.joystick, j))
                        for k in range(0, 5):
                            past_frame = port_frame_by_index(player_port, i - j - k, self.all_frames)
                            if past_frame.post.state == ActionState.KNEE_BEND:
                                self.wavedashes[-1].r_frame = k
                                self.wavedashes[-1].waveland = False
                                break
                        break
    
    def dashdance_compute(self, connect_code: str):
        player_port = None
        for player in self.players:
            if player.code == connect_code.upper():
                player_port = player.port
                break
        
        is_dashing = False

        for i, frame in enumerate(self.all_frames):
            player_frame = frame.ports[player_port].leader
            player_state = player_frame.post.state
            
            if player_state == ActionState.DASH:
                is_dashing = True
                self.dashes.append(DashData(player_frame.post.position.x))
                self.dashes
                if (port_frame_by_index(player_port, i - 1, self.all_frames).post.state == ActionState.WAIT and
                    port_frame_by_index(player_port, i - 2, self.all_frames).post.state == ActionState.DASH):
                    self.dashes[-1].is_dashdance = True
            else: 
                if is_dashing:
                    self.dashes[-1].end_pos = player_frame.post.position.x
                    is_dashing = False
    
    def opening_compute(self, connect_code:str):
        pass

    def tech_compute(self, connect_code:str):
        pass