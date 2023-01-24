from typing import List, Optional, Union, Tuple, Dict
from os import PathLike
from enum import Enum

from .game import Game
from .event import Frame, StateFlags, Start
from .id import ActionState, ActionRange, Stage
from .util import Base
from .metadata import Metadata


class ComputerBase(Base):

    rules: Optional[Start]
    players: List[Metadata.Player]
    all_frames: List[Frame]
    metadata: Optional[Metadata]
    queue: List[Dict]
    replay_path: PathLike | str

    def prime_replay(self, replay: PathLike | Game | str, retain_data=False) -> None:
        """Parses a replay and loads the relevant data into the combo computer. Call combo_compute(connect_code) to extract combos
        from parsed replay"""
        if isinstance(replay, PathLike) or isinstance(replay, str):
            parsed_replay = Game(replay)
            self.replay_path = replay
        if isinstance(replay, Game):
            parsed_replay = replay
            self.replay_path = ""

        self.rules = parsed_replay.start
        self.players = [player for player in parsed_replay.metadata.players if player is not None]
        # if len(self.players) > 2: raise Exception("Combo compute handles replays with a maximum of 2 players")
        self.all_frames = parsed_replay.frames
        self.metadata = parsed_replay.metadata
        
        if not retain_data:
            self.reset_data()

    def generate_player_ports(self, connect_code=None) -> List | Tuple:
        if connect_code:
            for i, player in enumerate(self.players):
                if player.connect_code == connect_code.upper():
                    player_port = [i]
                else:
                    opponent_port = i
            return player_port, opponent_port
        else:
        # If there's no connect code, extract the port values of both *active* ports
            player_ports = [i - 1 for i, x in enumerate(self.rules.players) if x is not None]
        # And if there's more than 2 active ports, we return an empty list which should skip processing. 
        # TODO make this an exception, but one that doesn't kill the program? Or just some way to track which replays don't get processed
            if len(player_ports) > 2:
                return []
            return player_ports
        
    def port_frame(self, port:int, frame: Frame):
        return frame.ports[port].leader
    
    def port_frame_by_index(self, port: int, index: int):
        return self.all_frames[index].ports[port].leader
    
    def reset_data(self):
        return
    


# Action state ranges are listed in id.py

def is_damaged(action_state: int) -> bool:
    """Recieves action state, returns whether or not the player is in a damaged state.
    This includes all generic variants."""
    return (ActionRange.DAMAGE_START <= action_state <= ActionRange.DAMAGE_END)

def is_in_hitstun(flags: StateFlags) -> bool:
    """Recieves StateFlags, returns whether or not the hitstun bitflag is active.
    Always returns false on older replays that do not support stateflags."""
    if StateFlags.HIT_STUN in flags:
        return True
    else:
        return False

def is_in_hitlag(flags: StateFlags) -> bool:
    """Recieves StateFlags, returns whether or not the hitlag bitflag is active.
    Always returns false on older replays that do not support stateflags."""
    if StateFlags.HIT_LAG in flags:
        return True
    else:
        return False

def is_grabbed(action_state: int) -> bool:
    return (ActionRange.CAPTURE_START <= action_state <= ActionRange.CAPTURE_END)

def is_cmd_grabbed(action_state: int) -> bool:
    """Reieves action state, returns whether or not player is command grabbed (falcon up b, kirby succ, cargo throw, etc)"""
    #Includes sing, bury, ice, cargo throw, mewtwo side B, koopa claw, kirby suck, and yoshi egg
    return (((ActionRange.COMMAND_GRAB_RANGE1_START <= action_state <= ActionRange.COMMAND_GRAB_RANGE1_END)
        or (ActionRange.COMMAND_GRAB_RANGE2_START <= action_state <= ActionRange.COMMAND_GRAB_RANGE2_END))
        and not action_state == ActionState.BARREL_WAIT)

def is_teching(action_state: int) -> bool:
    """Recieves action state, returns whether or not it falls into the tech action states, includes walljump/ceiling techs"""
    return (ActionRange.TECH_START <= action_state <= ActionRange.TECH_END or
    action_state == ActionState.FLY_REFLECT_CEIL or
    action_state == ActionState.FLY_REFLECT_WALL)

def is_dying(action_state: int) -> bool:
    """Reieves action state, returns whether or not player is in the dying animation from any blast zone"""
    return (ActionRange.DYING_START <= action_state <= ActionRange.DYING_END)

def is_downed(action_state: int) -> bool:
    """Recieves action state, returns whether or not player is downed (i.e. missed tech)"""
    return (ActionRange.DOWN_START <= action_state <= ActionRange.DOWN_END)

def is_offstage(curr_frame: Frame.Port.Data.Post, stage) -> bool:
    """Recieves current frame and stage ID, returns whether or not the player is outside the X coordinates denoting the on-stage bounds"""
    stage_bounds = [0, 0]

    # I manually grabbed these values using uncle punch and just moving as close to the edge as I could and rounding away from 0.
    # They don't cover 100% of cases (such as being underneath BF), but it's accurate enough for most standard edgeguard situations
    # In the future I'll add a Y value check, but i'll handle that when i handle ading Y value for juggles.
    match stage:
        case Stage.FOUNTAIN_OF_DREAMS:
            stage_bounds = [-64, 64]
        case Stage.YOSHIS_STORY:
            stage_bounds = [-56, 56]
        case Stage.DREAM_LAND_N64:
            stage_bounds = [-73, 73]
        case Stage.POKEMON_STADIUM:
            stage_bounds = [-88, 88]
        case Stage.BATTLEFIELD:
            stage_bounds = [-67, 67]
        case Stage.FINAL_DESTINATION:
            stage_bounds = [-89, 89]

    return (curr_frame.position.x < stage_bounds[0] or curr_frame.position.x > stage_bounds[1])

def is_shielding(action_state: int) -> bool:
    """Recieves action state, returns whether or not it falls into the guard action states"""
    return (ActionRange.GUARD_START <= action_state <= ActionRange.GUARD_END)

def is_shield_broken(action_state: int) -> bool:
    """Recieves action state, returns whether or not it falls into the guard_break action states"""
    return (ActionRange.GUARD_BREAK_START <= action_state <= ActionRange.GUARD_BREAK_END)

def is_dodging(action_state: int) -> bool:
    """Recieves action state and returns whether or not it falls into the 'dodging' category.
    Category includes shielded escape options (roll, spot dodge, airdodge)"""
    return (ActionRange.DODGE_START <= action_state <= ActionRange.DODGE_END)

def did_lose_stock(curr_frame: Frame.Port.Data.Post, prev_frame: Frame.Port.Data.Post) -> bool:
    """Recieves current and previous frame, returns stock difference between the two"""
    if not curr_frame or  not prev_frame:
        return False
    return prev_frame.stocks_remaining - curr_frame.stocks_remaining > 0

def calc_damage_taken(curr_frame: Frame.Port.Data.Post, prev_frame: Frame.Port.Data.Post) -> float:
    """Recieves current and previous frames, returns float of the difference in damage between the two"""
    percent = curr_frame.percent
    prev_percent = prev_frame.percent

    return percent - prev_percent

def is_ledge_action(action_state: int):
    """Recieves action state, returns whether or not player is currently hanging from the ledge, or doing any ledge action."""
    return ActionRange.LEDGE_ACTION_START <= action_state <= ActionRange.LEDGE_ACTION_END

def is_wavedashing(action_state: int, port:int,  frame_index: int, all_frames: List[Frame]) -> bool:
    if action_state != ActionState.ESCAPE_AIR:
        return False
    for i in range(1, 4):
        if (all_frames[frame_index - i].ports[port].leader.post.state == ActionState.LAND_FALL_SPECIAL):
            return True
    return False

def get_death_direction(action_state: int) -> str:
    match action_state:
        case 0:
            return "Bottom"
        case 1:
            return "Left"
        case 2:
            return "Right"
        case 3, 4, 5, 6, 7, 8, 9, 10:
            return "Top"
        case _:
            return "Invalid Action State"

class TechType(Enum):
    TECH_IN_PLACE = 0
    TECH_LEFT = 1
    TECH_RIGHT = 2
    GET_UP_ATTACK = 3
    MISSED_TECH = 4
    WALL_TECH = 5
    MISSED_WALL_TECH = 6
    WALL_JUMP_TECH = 7
    CEILING_TECH = 8
    MISSED_CEILING_TECH = 9
    JAB_RESET = 10

def get_tech_type(action_state: int, direction) -> TechType:
    match action_state:
        case ActionState.PASSIVE | ActionState.DOWN_STAND_U | ActionState.DOWN_STAND_D:
            return TechType.TECH_IN_PLACE
        case ActionState.PASSIVE_STAND_F | ActionState.DOWN_FOWARD_U | ActionState.DOWN_FOWARD_D:
            if direction > 0: return TechType.TECH_RIGHT
            else: return TechType.TECH_LEFT
        case ActionState.PASSIVE_STAND_B | ActionState.DOWN_BACK_U | ActionState.DOWN_BACK_D:
            if direction > 0: return TechType.TECH_LEFT
            else: return TechType.TECH_RIGHT
        case ActionState.DOWN_ATTACK_U | ActionState.DOWN_ATTACK_D:
            return TechType.GET_UP_ATTACK
        case ActionState.DOWN_BOUND_U | ActionState.DOWN_BOUND_D | ActionState.DOWN_WAIT_D | ActionState.DOWN_WAIT_U:
            return TechType.MISSED_TECH
        case ActionState.DOWN_DAMAGE_U | ActionState.DOWN_DAMAGE_D:
            return TechType.JAB_RESET
        case ActionState.PASSIVE_WALL:
            return TechType.WALL_TECH
        case ActionState.PASSIVE_WALL_JUMP:
            return TechType.WALL_JUMP_TECH
        case ActionState.PASSIVE_CEIL:
            return TechType.CEILING_TECH
        case _:
            return None
    


        
        