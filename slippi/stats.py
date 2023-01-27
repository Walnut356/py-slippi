from typing import Optional
from math import atan2, degrees

from .util import Base, try_enum
from .id import ActionState
from .event import Position, Buttons, Direction, Attack
from .common import *

class WavedashData(Base):
    port: int
    connect_code: Optional[str]
    r_frame: int # which airborne frame was the airdodge input on?
    angle: float # in degrees
    airdodge_frames: int
    waveland: bool

    def __init__(self, port, connect_code:Optional[str], r_input_frame:int=0, angle:Optional[Position]=None, airdodge_frames:int=0):
        self.port = port
        self.r_frame = r_input_frame
        if angle:
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
    port: int
    connect_code: Optional[str]
    start_pos: float
    end_pos: float
    direction: Direction
    is_dashdance: bool

    def __init__(self, port, connect_code:Optional[str], start_pos=0, end_pos = 0):
        self.port = port
        self.connect_code = connect_code
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.is_dashdance = False

    def distance(self) -> float:
        return abs(self.end_pos - self.start_pos)
    

class DashState(Base):
    dash: DashData
    active_dash: bool
    
    def __init__(self, port, connect_code:Optional[str]=None):
        self.dash = DashData(port, connect_code)
        self.active_dash = False

class TechData(Base):
    port: int
    connect_code: Optional[str]
    tech_type: Optional[TechType]
    direction: Direction
    position: Position
    is_on_platform: bool
    is_missed_tech: bool
    towards_center: Optional[bool]
    towards_opponent: Optional[bool]
    jab_reset: Optional[bool]
    last_hit_by: str

    def __init__(self, port, connect_code:Optional[str]=None):
        self.port = port
        self.connect_code = connect_code
        self.tech_type = None
        self.is_missed_tech = False
        self.towards_center = None
        self.towards_opponent = None
        self.jab_reset = None

class TechState(Base):
    tech: TechData
    last_state: Optional[ActionState | int]
    
    def __init__(self, port, connect_code:Optional[str]=None):
        self.tech = TechData(port, connect_code)
        self.last_state = None

class Data(Base):
    wavedashes: list[WavedashData]
    dashes: list[DashData]
    techs: list[TechData]

    def __init__(self):
        self.wavedashes = []
        self.dashes = []
        self.techs = []



class StatsComputer(ComputerBase):

    data: Data
    tech_state: Optional[TechState]
    dash_state: Optional[DashState]
    
    def __init__(self):
        self.data = Data()
        self.tech_state = None
        self.dash_state = None

    def reset_data(self):
        self.wavedashes = []
        self.dashes = []
        self.techs = []

    def stats_compute (self, connect_code: str, wavedash=True, dash=True, tech=True):
        if wavedash:
            self.wavedash_compute(connect_code)
        if dash:
            self.dash_compute(connect_code)
        if tech:
            self.tech_compute(connect_code)

    def wavedash_compute(self, connect_code:Optional[str]=None) -> list[WavedashData]:
        player_ports: list[int]
        opponent_port: int
        
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
                if player_state != ActionState.LAND_FALL_SPECIAL:
                    continue
                    
                if prev_player_frame.post.state == ActionState.LAND_FALL_SPECIAL:
                    continue

                # If we're in landfallspecial and weren't previously in landfallspecial:
                for j in reversed(range(0, 5)): # We reverse this range to search for the first instance of L or R
                    past_frame = self.port_frame_by_index(player_port, i - j)
                    if (Buttons.Physical.R in past_frame.pre.buttons.physical.pressed() or
                        Buttons.Physical.L in past_frame.pre.buttons.physical.pressed()):
                        self.data.wavedashes.append(WavedashData(player_port, connect_code, 0, player_frame.pre.joystick, j))

                        for k in range(0, 5):
                            past_frame = self.port_frame_by_index(player_port, i - j - k)
                            if past_frame.post.state == ActionState.KNEE_BEND:
                                self.data.wavedashes[-1].r_frame = k
                                self.data.wavedashes[-1].waveland = False
                                break
                        break
        return self.data.wavedashes
    
    def dash_compute(self, connect_code:Optional[str]=None) -> list[DashData]:
        player_ports = None
        opponent_port = None
        
        if connect_code:
            player_ports, opponent_port = self.generate_player_ports(connect_code)
        else:
            player_ports = self.generate_player_ports()

        for port_index, player_port in enumerate(player_ports):
            if len(player_ports) == 2:
                opponent_port = player_ports[port_index - 1] # Only works for 2 ports
            
            self.dash_state = DashState(player_port, connect_code)
            
            for i, frame in enumerate(self.all_frames):
                player_frame = self.port_frame(player_port, frame)
                player_state = player_frame.post.state
                prev_player_frame = self.port_frame_by_index(player_port, i - 1)
                prev_player_state = prev_player_frame.post.state
                prev_prev_player_frame = self.port_frame_by_index(player_port, i - 2)
                prev_prev_player_state = prev_prev_player_frame.post.state
                
                # if last 2 states weren't dash and curr state is dash, start dash event
                # if the state pattern dash -> wait -> dash occurs, mark as dashdance
                # if prev prev state was dash, prev state was not dash, and curr state isn't dash, end dash event

                if player_state == ActionState.DASH:
                    if prev_player_state != ActionState.DASH and prev_prev_player_frame != ActionState.DASH:
                        self.dash_state.dash = DashData(player_port, connect_code)
                        self.dash_state.active_dash = True
                        self.dash_state.dash.direction = player_frame.post.facing_direction
                        self.dash_state.dash.start_pos = player_frame.post.position.x
                    
                    if prev_player_state == ActionState.TURN and prev_prev_player_state == ActionState.DASH:
                        # if a dashdance pattern (dash -> turn -> dash) is detected, first we need to finalize and record the previous dash
                        self.dash_state.dash.end_pos = prev_prev_player_frame.post.position.x
                        self.data.dashes.append(self.dash_state.dash)
                        # then we need to create a new dash and update its information
                        self.dash_state.dash = DashData(player_port, connect_code)
                        self.dash_state.active_dash = True
                        self.dash_state.dash.direction = player_frame.post.facing_direction
                        self.dash_state.dash.start_pos = player_frame.post.position.x
                        self.dash_state.dash.is_dashdance = True
                    
                else:
                    # If not dashing for 2 consecutive frames, finalize the dash and reset the state
                    if (self.dash_state.active_dash and
                        prev_player_state != ActionState.DASH and prev_prev_player_state != ActionState.DASH):
                        self.dash_state.dash.end_pos = prev_prev_player_frame.post.position.x
                        self.data.dashes.append(self.dash_state.dash)
                        self.dash_state.active_dash = False
                        self.dash_state.dash = DashData(player_port, connect_code)
        return self.data.dashes

    def tech_compute(self, connect_code:Optional[str]=None) -> list[TechData]:
        player_ports: list[int]
        opponent_port: int
        
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
                        self.techs.append(self.tech_state.tech)
                        self.tech_state = None
                    continue

                opponent_frame = self.port_frame(opponent_port, frame).post

            # If we are, create a tech event, and start filling out fields based on the info we have
                if not was_teching:
                    self.tech_state = TechState(player_port, connect_code)
                    self.tech_state.tech.last_hit_by = try_enum(Attack, opponent_frame.most_recent_hit).name
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
        return self.data.techs


    # def sdi_compute(self, connect_code:str):
    #     player_ports: list[int]
    #     opponent_port: int
        
    #     if connect_code:
    #             player_ports, opponent_port = self.generate_player_ports(connect_code)
    #     else:
    #         player_ports = self.generate_player_ports()

    #     for port_index, player_port in enumerate(player_ports):
    #         if len(player_ports) == 2:
    #             opponent_port = player_ports[port_index - 1] # Only works for 2 ports

    #         for i, frame in enumerate(self.all_frames):
    #             player_frame = self.port_frame(player_port, frame)


    #             if player_frame.post:
    #                 pass