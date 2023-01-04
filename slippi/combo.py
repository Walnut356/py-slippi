from typing import List, Dict, Optional

from .util import *
from .game import Game
from .id import ActionState, Stage
from .event import Start, Frame, StateFlags
from .metadata import Metadata


COMBO_LENIENCY = 45

class ComboEvent(Enum):
    """Enumeration for combo states, maybe unused?"""
    COMBO_START = "COMBO_START"
    COMBO_EXTEND = "COMBO_EXTEND"
    COMBO_END = "COMBO_END"
  
class MoveLanded(Base):
    """Contains all data for a single move connecting"""
    player: str = ""
    frame: int = 0
    move_id: int = 0
    hit_count: int = 0
    damage: float = 0.0

class ComboData(Base):
    "Contains a single complete combo, including movelist"
    player: str = ""
    moves: List[MoveLanded] = []
    did_kill: bool = False
    start_percent: float = 0.0
    current_percent: float = 0.0
    end_percent: float = 0.0
    start_frame: int = 0
    end_frame: int = 0

class ComboState(Base):
    combo: Optional[ComboData] = ComboData()
    move: Optional[MoveLanded] = MoveLanded()
    reset_counter: int = 0
    last_hit_animation = None
    event: ComboEvent = None
 
class PlayerIndex(Base):
    player: Start.Player
    code: str
    port: int
   
    def __init__(self, player, code, port):
        self.player = player
        self.code = code
        self.port = port

class ComboComputer(Base):
    """Base class for parsing combo events, call .prime_replay(path) to set up the instance,
    and .combo_compute(connect_code) to populate the computer's .combos list. """
    rules: Optional[Start]
    combos: List[ComboData]
    players: List[PlayerIndex]
    all_frames: List[Frame]
    combo_state: Optional[ComboState]
    metadata: Optional[Metadata]

    def __init__(self):
        self.rules = None
        self.combos = []
        self.players = []
        self.all_frames = []
        self.combo_state = None
        self.metadata = None
    
    def prime_replay(self, replay_path):
        parsed_replay = Game(replay_path)
        self.rules = parsed_replay.start
        for i in range(0,2):
            self.players.append(PlayerIndex(parsed_replay.start.players[i], parsed_replay.metadata.players[i].connect_code, i))
        self.combos = []
        self.all_frames = parsed_replay.frames
        self.combo_state = ComboState()
        self.metadata = parsed_replay.metadata

    def combo_compute(self, connect_code: str):
    # Most people want combos from a specific player, so forcing a connect code requirement
    # will cover most usecases
        player_port = None
        opponent_port = None
        for player in self.players:
            if player.code == connect_code:
                player_port: int = player.port
            else:
                opponent_port: int = player.port
                
        # TODO add handling for connect code not found

        for i, frame in enumerate(self.all_frames):
        # player data is stored as list of frames -> individual frame -> port -> leader/follower -> pre/post frame data
        # we make an interface as soon as possible because that's awful
            player_frame: Frame.Port.Data.Post = frame.ports[player_port].leader.post
            opponent_frame: Frame.Port.Data.Post = frame.ports[opponent_port].leader.post
            
        # Frames are -123 indexed, so we can't just pull the frame's .index to acquire the previous frame
        # this is the sole reason for enumerating self.all_frames
            prev_player_frame: Frame.Port.Data.Post = self.all_frames[i - 1].ports[player_port].leader.post
            prev_opponent_frame: Frame.Port.Data.Post = self.all_frames[i - 1].ports[opponent_port].leader.post
            
            opnt_action_state = opponent_frame.state
            opnt_is_damaged = is_damaged(opnt_action_state)
            opnt_is_in_hitstun = is_in_hitstun(opponent_frame.flags) # Bitflags are used because the hitstun frame count is used for a bunch of other things as well
            opnt_is_in_hitlag = is_in_hitlag(opponent_frame.flags)
            opnt_is_grabbed = is_grabbed(opnt_action_state)
            opnt_is_cmd_grabbed = is_cmd_grabbed(opnt_action_state)
            opnt_is_teching = is_teching(opnt_action_state)
            opnt_is_downed = is_downed(opnt_action_state)
            opnt_is_dying = is_dying(opnt_action_state)
            opnt_is_offstage = is_offstage(opponent_frame, self.rules.stage)
            opnt_is_dodging = is_dodging(opnt_action_state)
            opnt_is_shielding = is_shielding(opnt_action_state)
            opnt_is_shield_broken = is_shield_broken(opnt_action_state)
            opnt_damage_taken = calc_damage_taken(opponent_frame, prev_opponent_frame)
            opnt_did_lose_stock = did_lose_stock(opponent_frame, prev_opponent_frame)
            opnt_is_ledge_action = is_ledge_action(opnt_action_state)

        # "Keep track of whether actionState changes after a hit. Used to compute move count
        # When purely using action state there was a bug where if you did two of the same
        # move really fast (such as ganon's jab), it would count as one move. Added
        # the actionStateCounter at this point which counts the number of frames since
        # an animation started. Should be more robust, for old files it should always be
        # null and null < null = false" - official parser
            action_changed_since_hit = not (player_frame.state == self.combo_state.last_hit_animation)
            action_frame_counter = player_frame.state_age
            prev_action_counter = prev_player_frame.state_age
            action_state_reset = action_frame_counter < prev_action_counter
            if(action_changed_since_hit or action_state_reset):
                self.combo_state.last_hit_animation = None
            
            
        # I throw in the extra hitstun check to make it extra robust in case the animations are weird for whatever reason
        # Don't include hitlag check unless you want shield hits to start combo events.
        # There might be false positives on self damage like fully charged 
            if (opnt_is_damaged or
                opnt_is_grabbed or
                opnt_is_cmd_grabbed or
                opnt_is_in_hitstun):
                
                combo_started = False

            # if the opponent has been hit and 
                if self.combo_state.combo is None:
                    self.combo_state.combo = ComboData()
                    self.combo_state.combo.player = self.players[player_port].code
                    self.combo_state.combo.moves = []
                    self.combo_state.combo.did_kill = False
                    self.combo_state.combo.start_frame = frame.index
                    self.combo_state.combo.end_frame = None
                    self.combo_state.combo.start_percent = prev_opponent_frame.damage
                    self.combo_state.combo.current_percent = opponent_frame.damage
                    self.combo_state.combo.end_percent = opponent_frame.damage
                    
                    self.combos.append(self.combo_state.combo)
                    
                    combo_started = True
                
                if opnt_damage_taken:
                    if self.combo_state.last_hit_animation is None:
                        self.combo_state.move = MoveLanded()
                        self.combo_state.move.player = self.players[player_port].code
                        self.combo_state.move.frame = frame.index
                        self.combo_state.move.move_id = player_frame.last_attack_landed
                        self.combo_state.move.hit_count = 0
                        self.combo_state.move.damage = 0
                        
                        self.combo_state.combo.moves.append(self.combo_state.move)
                    
                        if not combo_started:
                            self.combo_state.event = ComboEvent.COMBO_EXTEND
                    
                    if self.combo_state.move:
                        self.combo_state.move.hit_count += 1
                        self.combo_state.move.damage += opnt_damage_taken
                
                    self.combo_state.last_hit_animation = prev_player_frame.state
            
                if combo_started:
                    self.combo_state.event = ComboEvent.COMBO_START
        
        # if a combo hasn't started and no damage was taken this frame, just skip to the next frame
            if self.combo_state.combo is None:
                continue
            
            if not opnt_did_lose_stock:
                self.combo_state.combo.current_percent = opponent_frame.damage

        # reset the combo timeout timer to 0 if the opponent meets the following conditions
        # list expanded from official parser to allow for higher combo variety and capture more of what we would count as "combos"
        # noteably, this list will allow mid-combo shield pressure and edgeguards to be counted as part of a combo
        # TODO add interface to disable/enable these checks? (argument && is_X check)
            if (opnt_is_damaged or # Action state range
                opnt_is_grabbed or # Action state range
                opnt_is_cmd_grabbed or # Action state range
                opnt_is_in_hitlag or # Bitflags (will always fail with old replays)
                opnt_is_in_hitstun or # Bitflags (will always fail with old replays)
                opnt_is_shielding or # Action state range
                opnt_is_offstage or # X coordinate check
                opnt_is_dodging or # Action state range
                opnt_is_dying or # Action state range
                opnt_is_downed or # Action state check
                opnt_is_teching or
                opnt_is_ledge_action or
                opnt_is_shield_broken): # Action state check
                
                self.combo_state.reset_counter = 0
            else: 
                self.combo_state.reset_counter += 1
            
            should_terminate = False
            
        # All combo end checks below
            if opnt_did_lose_stock:
                self.combo_state.combo.did_kill = True
                should_terminate = True
            
            if self.combo_state.reset_counter > COMBO_LENIENCY:
                should_terminate = True
            
        # If the combo should end, finalize the values, reset the temp storage
            if should_terminate:
                self.combo_state.combo.end_frame = frame.index
                self.combo_state.combo.end_percent = prev_opponent_frame.damage
                self.combo_state.event = ComboEvent.COMBO_END # not entirely convinced these do anything, even in the official parser?

                
                self.combo_state.combo = None
                self.combo_state.move = None
            

# It's probably worth spliting these off into a seperate file similar to the official parser
# if i end up adding more stats calculators, but for now i'd rather keep the file structure cleaner

def is_damaged(action_state) -> bool:
    return (ActionState.DAMAGE_START <= action_state <= ActionState.DAMAGE_END)

def is_in_hitstun(flags) -> bool:
    if StateFlags.HIT_STUN in flags:
        return True
    else: 
        return False

def is_in_hitlag(flags) -> bool:
    if StateFlags.HIT_LAG in flags:
        return True
    else:
        return False

def is_grabbed(action_state) -> bool:
    return (ActionState.CAPTURE_START <= action_state <= ActionState.CAPTURE_END)

def is_cmd_grabbed(action_state) -> bool:
    return (((ActionState.COMMAND_GRAB_RANGE1_START <= action_state <= ActionState.COMMAND_GRAB_RANGE1_END)
        or (ActionState.COMMAND_GRAB_RANGE2_START <= action_state <= ActionState.COMMAND_GRAB_RANGE2_END))
        and not action_state == ActionState.BARREL_WAIT)

def is_teching(action_state) -> bool:
    return (ActionState.TECH_START <= action_state <= ActionState.TECH_END)

def is_dying(action_state) -> bool:
    return (ActionState.DYING_START <= action_state <= ActionState.DYING_END)

def is_downed(action_state) -> bool:
    return (ActionState.DOWN_START <= action_state <= ActionState.DOWN_END)

def is_offstage(curr_frame: Frame.Port.Data.Post, stage) -> bool:
    stage_bounds = [0, 0]

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

    if (curr_frame.position.x < stage_bounds[0] or
        curr_frame.position.x > stage_bounds[1]):
        return True

    else:
        return False

def is_shielding(action_state) -> bool:
    return (ActionState.GUARD_START <= action_state <= ActionState.GUARD_END)

def is_shield_broken(action_state) -> bool:
    return (ActionState.GUARD_BREAK_START <= action_state <= ActionState.GUARD_BREAK_END)

def is_dodging(action_state) -> bool:
    return (ActionState.DODGE_START <= action_state <= ActionState.DODGE_END)


def did_lose_stock(curr_frame: Frame.Port.Data.Post, prev_frame: Frame.Port.Data.Post) -> bool:
    if not curr_frame or  not prev_frame:
        return False

    return prev_frame.stocks - curr_frame.stocks > 0

def calc_damage_taken(curr_frame: Frame.Port.Data.Post, prev_frame: Frame.Port.Data.Post) -> float:
    percent = curr_frame.damage
    prev_percent = prev_frame.damage

    return percent - prev_percent

def is_ledge_action(action_state: int):
    return ActionState.LEDGE_ACTION_START <= action_state <= ActionState.LEDGE_ACTION_END
