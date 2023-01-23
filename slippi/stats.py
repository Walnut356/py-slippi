from typing import List, Dict, Optional, Union
from pathlib import Path
from math import atan2, degrees

from .util import Base, try_enum
from .game import Game
from .id import ActionState, Stage
from .event import Start, Frame, StateFlags, Position, Buttons, Direction, Attack
from .metadata import Metadata
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
    tech_type: TechType
    position: Position
    is_on_platform: bool
    is_missed_tech: bool
    towards_center: Optional[bool]
    towards_opponent: Optional[bool]
    jab_reset: Optional[bool]
    last_hit_by: Attack

    def __init__(self):
        self.tech_type = None
        self.is_missed_tech = False
        self.towards_center = None
        self.towards_opponent = None
        self.jab_reset = None

class TechState(Base):
    tech: TechData
    last_state: ActionState | int
    finalize: bool


class StatsComputer(ComputerBase):
    rules: Optional[Start]
    players: List[Metadata.Player]
    all_frames: List[Frame]
    metadata: Optional[Metadata]
    wavedashes: List[WavedashData]
    dashes: List[DashData]
    techs: List[TechData]
    tech_state: Optional[TechState]
    
    def __init__(self):
        self.rules = None
        self.players = []
        self.all_frames = []
        self.metadata = None
        self.wavedashes = []
        self.dashes = []

    def reset_data(self):
        self.wavedashes = []
        self.dashes = []
        self.techs = []

    def wavedash_compute(self, connect_code: str):
        player_ports = None
        opponent_port = None
        
        if connect_code:
            player_ports, opponent_port = self.generate_player_ports(connect_code)
        else:
            player_ports = self.generate_player_ports()
            
        for port_index, player_port in enumerate(player_ports):
            if len(player_ports) == 2:
                opponent_port = player_ports[port_index - 1] # Only works for 2 ports

            for i, frame in enumerate(self.all_frames):
                player_frame = self.port_frame(player_port, frame)
                player_state = player_frame.post.state
                prev_player_frame = self.port_frame_by_index(player_port, i - 1)

                #TODO add wavesurf logic? 
                if player_state == ActionState.LAND_FALL_SPECIAL and prev_player_frame.post.state != ActionState.LAND_FALL_SPECIAL:
                    for j in reversed(range(0, 5)):
                        past_frame = self.port_frame_by_index(player_port, i - j)
                        if Buttons.Physical.R in past_frame.pre.buttons.physical.pressed() or Buttons.Physical.L in past_frame.pre.buttons.physical.pressed():
                            self.wavedashes.append(WavedashData(0, player_frame.pre.joystick, j))
                            for k in range(0, 5):
                                past_frame = self.port_frame_by_index(player_port, i - j - k)
                                if past_frame.post.state == ActionState.KNEE_BEND:
                                    self.wavedashes[-1].r_frame = k
                                    self.wavedashes[-1].waveland = False
                                    break
                            break
    
    def dash_compute(self, connect_code: str):
        player_ports = None
        opponent_port = None
        
        if connect_code:
            player_ports, opponent_port = self.generate_player_ports(connect_code)
        else:
            player_ports = self.generate_player_ports()

        is_dashing = False

        for port_index, player_port in enumerate(player_ports):
            if len(player_ports) == 2:
                opponent_port = player_ports[port_index - 1] # Only works for 2 ports

            for i, frame in enumerate(self.all_frames):
                player_frame = self.port_frame(player_port, frame)
                player_state = player_frame.post.state
                
                if player_state == ActionState.DASH:
                    is_dashing = True
                    self.dashes.append(DashData(player_frame.post.position.x))
                    self.dashes
                    # The pattern dash -> wait -> dash should catch all dash dances, fox trots will count as 2 different dash instances
                    if (self.port_frame_by_index(player_port, i - 1).post.state == ActionState.WAIT and
                        self.port_frame_by_index(player_port, i - 2).post.state == ActionState.DASH):
                        self.dashes[-1].is_dashdance = True
                else: 
                    if is_dashing:
                        self.dashes[-1].end_pos = player_frame.post.position.x
                        is_dashing = False
    
    

    def tech_compute(self, connect_code:str):
        player_ports = None
        opponent_port = None
        
        if connect_code:
            player_ports, opponent_port = self.generate_player_ports(connect_code)
        else:
            player_ports = self.generate_player_ports()

        for port_index, player_port in enumerate(player_ports):
            if len(player_ports) == 2:
                opponent_port = player_ports[port_index - 1] # Only works for 2 ports

            for i, frame in enumerate(self.all_frames):
                player_frame = self.port_frame(player_port, frame).post
                player_state = player_frame.state
                prev_player_frame = self.port_frame_by_index(player_port, i - 1).post
                prev_player_state = prev_player_frame.state

                

                curr_teching = is_teching(player_state)
                was_teching = is_teching(prev_player_state)
            
            # Close out active techs if we were teching, and save some processing power if we weren't
                if not curr_teching:
                    if was_teching:
                        self.techs.append(TechState.tech)
                        self.tech_state = None
                    continue

                opponent_frame = self.port_frame(opponent_port, frame).post

            # If we are, create a tech event, and start filling out fields based on the info we have
                if not was_teching:
                    self.tech_state = TechState()
                    self.tech_state.tech.last_hit_by = try_enum(Attack, opponent_frame.most_recent_hit)
                    self.tech_state.tech.position = player_frame.position
                    self.tech_state.tech.is_on_platform = player_frame.position.y > 5 # Arbitrary value, i'll have to fact check this

                tech_type = get_tech_type(player_state, player_frame.facing_direction)

                self.tech_state.tech.tech_type = tech_type
                
                if player_state == self.tech_state.last_state:
                    continue

                self.tech_state.last_state = player_state

                match tech_type:
                    case TechType.MISSED_TECH, TechType.MISSED_WALL_TECH, TechType.MISSED_CEILING_TECH:
                        self.tech_state.tech.is_missed_tech = True
                        self.tech_state.tech.jab_reset = False

                    case TechType.JAB_RESET:
                        self.tech_state.tech.jab_reset = True
                    
                    case TechType.TECH_LEFT:
                        opnt_relative_position = opponent_frame.position.x - player_frame.position.x
                        if player_frame.facing_direction > 0:
                            self.tech_state.tech.towards_center = True
                        else:
                            self.tech_state.tech.towards_center = False
                        if opnt_relative_position > 0:
                            self.tech_state.tech.towards_opponent = True
                        else:
                            self.tech_state.tech.towards_opponent = False
                    case TechType.TECH_RIGHT:
                        opnt_relative_position = opponent_frame.position.x - player_frame.position.x
                        if player_frame.facing_direction > 0:
                            self.tech_state.tech.towards_center = False
                        else:
                            self.tech_state.tech.towards_center = True
                        if opnt_relative_position > 0:
                            self.tech_state.tech.towards_opponent = False
                        else:
                            self.tech_state.tech.towards_opponent = True
                    
                    case _: # Tech in place, getup attack
                        pass


                


                



    def opening_compute(self, connect_code:str):
        pass