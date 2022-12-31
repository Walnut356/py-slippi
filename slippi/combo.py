from .util import *
from .game import Game
from . import id as sid
from .event import Start, Frame
from typing import NewType


class ComboData:
    player_index = None
    moves = []
    did_kill = False
    
    start_percent = None
    end_percent = None
    
    start_frame = None
    end_frame = None

class ComboState:
    combo: ComboData
    move: int
    resetCounter: int = 0
    
class PlayerIndex:
    player: Start.Player
    code: str
    

class ComboComputer:
    rules: Start
    combos: list[ComboData]
    players: list[PlayerIndex]
    all_frames: list[Frame]
    
    def __init__(self, replay: Game):
        self.rules = replay.start
        for i in range(0,2):
            self.players.append(
                PlayerIndex(replay.start.players[i],
                replay.metadata.players[i].connect_code, i))
        self.combos