from .util import *
from .game import Game
from . import id as sid
from .event import Start, Frame, StateFlags

combo_leniency = 45

class ComboEvent(enum):
    COMBO_START = "COMBO_START"
    COMBO_EXTEND = "COMBO_EXTEND"
    COMBO_END = "COMBO_END"

class ComboData:
    player: str
    moves: list
    did_kill: bool
    
    start_percent: float
    end_percent: float
    
    start_frame: int
    end_frame: int
    
class MoveLanded:
    player: str
    frame: int
    move_id: int
    hit_count: int
    damage: float

class ComboState:
    combo: ComboData
    move: MoveLanded
    reset_counter: int = 0
    last_hit_animation: int
    event: ComboEvent
    
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
    
    def prime_replay(self, replay: Game):
        self.rules = replay.start
        for i in range(0,2):
            self.players.append(
                PlayerIndex(replay.start.players[i],
                replay.metadata.players[i].connect_code, i))
        self.combos = []
        self.all_frames = Game.frames
    
    def combo_compute(self, connect_code: str):
        for player in self.players:
            if player.code == connect_code:
                player_port: int = player.port
            else:
                opponent_port: int = player.port
        
        #add handling for connect code not found
        for frame in self.all_frames:
            player_frame = frame.ports[player_port].leader.post
            opponent_frame = frame.ports[opponent_port].leader.post
            
            prev_player_frame = self.all_frames[frame.index - 1].ports[player_port].leader.post
            prev_opponent_frame = self.all_frames[frame.index - 1].ports[opponent_port].leader.post
            
            opnt_action_state = opponent_frame.state
            opnt_is_damaged = is_damaged(opnt_action_state)
            opnt_is_in_hitstun = is_in_hitstun(opponent_frame.flags)
            opnt_is_in_hitlag = is_in_hitlag(opponent_frame.flags)
            opnt_is_grabbed = is_grabbed(opnt_action_state)
            opnt_is_cmd_grabbed = is_cmd_grabbed(opnt_action_state)
            opnt_is_teching = is_teching(opnt_action_state)
            opnt_is_downed = is_downed(opnt_action_state)
            opnt_is_dying = is_dying(opnt_action_state)
            opnt_is_offstage = is_offstage(opponent_frame, )
            opnt_is_dodging = is_dodging(opnt_action_state)
            opnt_is_shielding = is_shielding(opnt_action_state)
            opnt_is_shield_broken = is_shield_broken(opnt_action_state)
            opnt_damage_taken = calc_damage_taken(opponent_frame, prev_opponent_frame)
            opnt_did_lose_stock = did_lose_stock()
            
# Keep track of whether actionState changes after a hit. Used to compute move count
# When purely using action state there was a bug where if you did two of the same
# move really fast (such as ganon's jab), it would count as one move. Added
# the actionStateCounter at this point which counts the number of frames since
# an animation started. Should be more robust, for old files it should always be
# null and null < null = false
            action_changed_since_hit = (not player_frame.state is self.combo_state.last_hit_animation)
            action_counter = player_frame.state_age
            prev_action_counter = prev_player_frame.state_age
            action_state_reset = action_counter < prev_action_counter
            if(action_changed_since_hit or action_state_reset):
                self.combo_state.last_hit_animation = None
            
            
            if (opnt_is_damaged or
                opnt_is_grabbed or
                opnt_is_cmd_grabbed or
                opnt_is_in_hitlag or
                opnt_is_in_hitstun):
                
                comb_started = False
                if self.combo_state.combo.player is None:
                    self.combo_state.combo.player = player.code
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
                        self.combo_state.move.player = player.code
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
            
            if self.combo_state.reset_counter > combo_leniency:
                should_terminate = True
            
            if should_terminate:
                self.combo_state.combo.end_frame = frame.index
                self.combo_state.combo.end_percent = prev_opponent_frame.damage
                self.combo_state.event = ComboEvent.COMBO_END
                
                self.combo_state.combo = None
                self.combo_state.move = None



def is_damaged(action_state) -> bool:
    return (action_state >= 75 and action_state <= 91)

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
    pass

def is_cmd_grabbed(action_state) -> bool:
    pass

def calc_damage_taken(curr_frame, prev_frame) -> float:
    pass

def is_teching():
    pass

def is_dying():
    pass

def is_downed():
    pass

def is_offstage():
    pass

def is_shielding():
    pass

def is_shield_broken():
    pass

def is_dodging():
    pass

def did_lose_stock():
    pass