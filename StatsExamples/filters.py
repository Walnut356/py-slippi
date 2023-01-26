from typing import List

from slippi import *

def filter_direction(stats: List, direction: event.Direction):
    if hasattr(stats[0], "direction"):
        return [stat for stat in stats if stat.direction == direction]
    else:
        return stats

def filter_length(combos: List[combo.ComboData], min: int=0, max: int=100) -> List[combo.ComboData]:
    return [combo for combo in combos if min < len(combo.moves) < max]

def filter_damage(combos)