from .util import *
from .game import Game
from .id import ActionState, Stage
from .event import Start, Frame, StateFlags

COMBO_LENIENCY = 45

class ComboEvent(Enum):
    COMBO_START = "COMBO_START"
    COMBO_EXTEND = "COMBO_EXTEND"
    COMBO_END = "COMBO_END"
  
class MoveLanded:
    player: str = ""
    frame: int = 0
    move_id: int = 0
    hit_count: int = 0
    damage: float = 0.0

class ComboData:
    player: str = ""
    moves: list[MoveLanded] = []
    did_kill: bool = False
    start_percent: float = 0.0
    current_percent: float = 0.0
    end_percent: float = 0.0
    start_frame: int = 0
    end_frame: int = 0

class ComboState:
    combo: ComboData = ComboData()
    move: MoveLanded = MoveLanded()
    reset_counter: int = 0
    last_hit_animation = None
    event: ComboEvent = None
 
class PlayerIndex:
    player: Start.Player
    code: str
    port: int
   
    def __init__(self, player, code, port):
        self.player = player
        self.code = code
        self.port = port

class ComboComputer:
    rules: Start
    combos: list[ComboData]
    players: list[PlayerIndex]
    all_frames: list[Frame]
    combo_state: ComboState

    def __init__(self):
        self.rules = None
        self.combos = []
        self.players = []
        self.all_frames = []
        self.combo_state = None
    
    def prime_replay(self, replay_path):
        parsed_replay = Game(replay_path)
        self.rules = parsed_replay.start
        for i in range(0,2):
            self.players.append(PlayerIndex(parsed_replay.start.players[i], parsed_replay.metadata.players[i].connect_code, i))
        self.combos = []
        self.all_frames = parsed_replay.frames
        self.combo_state = ComboState()

    def combo_compute(self, connect_code: str):
        #assign port index to desired player via connect code
        for player in self.players:
            if player.code == connect_code:
                player_port: int = player.port
            else:
                opponent_port: int = player.port
        
        # TODO add handling for connect code not found
        
        for i, frame in enumerate(self.all_frames):
            # directly access individual port frame data
            player_frame = frame.ports[player_port].leader.post
            opponent_frame = frame.ports[opponent_port].leader.post
            # grab previous frame for future comparisons
            prev_player_frame = self.all_frames[i - 1].ports[player_port].leader.post
            prev_opponent_frame = self.all_frames[i - 1].ports[opponent_port].leader.post
            
            opnt_action_state = opponent_frame.state
            opnt_is_damaged = is_damaged(opnt_action_state)
            opnt_is_in_hitstun = is_in_hitstun(opponent_frame.flags)
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
            
# Keep track of whether actionState changes after a hit. Used to compute move count
# When purely using action state there was a bug where if you did two of the same
# move really fast (such as ganon's jab), it would count as one move. Added
# the actionStateCounter at this point which counts the number of frames since
# an animation started. Should be more robust, for old files it should always be
# null and null < null = false
            action_changed_since_hit = not (player_frame.state == self.combo_state.last_hit_animation)
            action_frame_counter = player_frame.state_age
            prev_action_counter = prev_player_frame.state_age
            action_state_reset = action_frame_counter < prev_action_counter
            if(action_changed_since_hit or action_state_reset):
                self.combo_state.last_hit_animation = None
            
            
            if (opnt_is_damaged or
                opnt_is_grabbed or
                opnt_is_cmd_grabbed or
                opnt_is_in_hitstun):
                
                combo_started = False
                if self.combo_state.combo is None:
                    self.combo_state.combo = ComboData()
                    self.combo_state.combo.player = self.players[player_port].code
                    self.combo_state.combo.moves = []
                    self.combo_state.combo.did_kill = False
                    self.combo_state.combo.start_frame = frame.index
                    self.combo_state.combo.end_frame = None
                    self.combo_state.combo.start_percent = prev_opponent_frame.damage
                    self.combo_state.combo.current_percent = opponent_frame.damage
                    self.combo_state.combo.end_percent = None
                    
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
        
            if not self.combo_state.combo:
                continue
            
            if not opnt_did_lose_stock:
                self.combo_state.combo.current_percent = opponent_frame.damage

            if (opnt_is_damaged or
                opnt_is_grabbed or
                opnt_is_cmd_grabbed or
                opnt_is_in_hitlag or
                opnt_is_in_hitstun or
                opnt_is_shielding or
                opnt_is_offstage or
                opnt_is_dodging or
                opnt_is_dying or
                opnt_is_downed or
                opnt_is_teching):
                
                self.combo_state.reset_counter = 0
            else: 
                self.combo_state.reset_counter += 1
            
            should_terminate = False
            
            if opnt_did_lose_stock:
                self.combo_state.combo.did_kill = True
                should_terminate = True
            
            if self.combo_state.reset_counter > COMBO_LENIENCY:
                should_terminate = True
            
            if should_terminate:
                self.combo_state.combo.end_frame = frame.index
                self.combo_state.combo.end_percent = self.combo_state.combo.current_percent
                self.combo_state.event = ComboEvent.COMBO_END
                
                self.combo_state.combo = None
                self.combo_state.move = None
            



def is_damaged(action_state) -> bool:
    return (action_state >= ActionState.DAMAGE_START and action_state <= ActionState.DAMAGE_END)

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
    return (action_state >= ActionState.CAPTURE_START and action_state <= ActionState.CAPTURE_END)

def is_cmd_grabbed(action_state) -> bool:
    return (((action_state >= ActionState.COMMAND_GRAB_RANGE1_START and action_state <= ActionState.COMMAND_GRAB_RANGE1_END)
        or (action_state >= ActionState.COMMAND_GRAB_RANGE2_START and action_state <= ActionState.COMMAND_GRAB_RANGE2_END))
        and not action_state is ActionState.BARREL_WAIT)

def is_teching(action_state) -> bool:
    return (action_state >= ActionState.TECH_START and action_state <= ActionState.TECH_END)

def is_dying(action_state) -> bool:
    return (action_state >= ActionState.DYING_START and action_state <= ActionState.DYING_END)

def is_downed(action_state) -> bool:
    return (action_state >= ActionState.DOWN_START and action_state <= ActionState.DOWN_END)

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
    return (action_state >= ActionState.GUARD_START and action_state <= ActionState.GUARD_END)

def is_shield_broken(action_state) -> bool:
    return (action_state >= ActionState.GUARD_BREAK_START and action_state <= ActionState.GUARD_BREAK_END)

def is_dodging(action_state) -> bool:
    return (action_state >= ActionState.DODGE_START and action_state <= ActionState.DODGE_END)

def did_lose_stock(curr_frame: Frame.Port.Data.Post, prev_frame: Frame.Port.Data.Post) -> bool:
    if not curr_frame or  not prev_frame:
        return False

    return (prev_frame.stocks - curr_frame.stocks) > 0

def calc_damage_taken(curr_frame: Frame.Port.Data.Post, prev_frame: Frame.Port.Data.Post) -> float:
    percent = curr_frame.damage
    prev_percent = prev_frame.damage

    return percent - prev_percent
