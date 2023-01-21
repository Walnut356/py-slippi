from typing import List

from .event import Frame, StateFlags
from .id import ActionState, Stage

# Action state ranges are listed in id.py

def is_damaged(action_state: int) -> bool:
    """Recieves action state, returns whether or not the player is in a damaged state.
    This includes all generic variants."""
    return (ActionState.DAMAGE_START <= action_state <= ActionState.DAMAGE_END)

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
    return (ActionState.CAPTURE_START <= action_state <= ActionState.CAPTURE_END)

def is_cmd_grabbed(action_state: int) -> bool:
    """Reieves action state, returns whether or not player is command grabbed (falcon up b, kirby succ, cargo throw, etc)"""
    #Includes sing, bury, ice, cargo throw, mewtwo side B, koopa claw, kirby suck, and yoshi egg
    return (((ActionState.COMMAND_GRAB_RANGE1_START <= action_state <= ActionState.COMMAND_GRAB_RANGE1_END)
        or (ActionState.COMMAND_GRAB_RANGE2_START <= action_state <= ActionState.COMMAND_GRAB_RANGE2_END))
        and not action_state == ActionState.BARREL_WAIT)

def is_teching(action_state: int) -> bool:
    """Recieves action state, returns whether or not it falls into the tech action states, includes walljump/ceiling techs"""
    return (ActionState.TECH_START <= action_state <= ActionState.TECH_END)

def is_dying(action_state: int) -> bool:
    """Reieves action state, returns whether or not player is in the dying animation from any blast zone"""
    return (ActionState.DYING_START <= action_state <= ActionState.DYING_END)

def is_downed(action_state: int) -> bool:
    """Recieves action state, returns whether or not player is downed (i.e. missed tech)"""
    return (ActionState.DOWN_START <= action_state <= ActionState.DOWN_END)

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
    return (ActionState.GUARD_START <= action_state <= ActionState.GUARD_END)

def is_shield_broken(action_state: int) -> bool:
    """Recieves action state, returns whether or not it falls into the guard_break action states"""
    return (ActionState.GUARD_BREAK_START <= action_state <= ActionState.GUARD_BREAK_END)

def is_dodging(action_state: int) -> bool:
    """Recieves action state and returns whether or not it falls into the 'dodging' category.
    Category includes shielded escape options (roll, spot dodge, airdodge)"""
    return (ActionState.DODGE_START <= action_state <= ActionState.DODGE_END)

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
    return ActionState.LEDGE_ACTION_START <= action_state <= ActionState.LEDGE_ACTION_END

def is_wavedashing(action_state: int, port:int,  frame_index: int, all_frames: List[Frame]) -> bool:
    if action_state != ActionState.ESCAPE_AIR:
        return False
    for i in range(1, 4):
        if (port_frame_by_index(port, frame_index + i, all_frames).post.state == ActionState.LAND_FALL_SPECIAL or
            port_frame_by_index(port, frame_index - i, all_frames).post.state == ActionState.KNEE_BEND):
            return True
    return False

def port_frame_by_index(port: int, index: int, all_frames: List[Frame]):
    return all_frames[index].ports[port].leader